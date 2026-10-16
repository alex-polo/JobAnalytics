"""Service for discovering vacancies and downloading raw vacancy data.

``DiscoveryService`` is the orchestrator for the discovery pipeline:

* register a discovery session per source,
* iterate keywords, call the source plugin to fetch vacancies,
* persist raw vacancies and enqueue them for matching/analysis,
* finalise the session as ``FINISHED`` or ``ERROR``.

Transaction strategy:

* HTTP calls to plugins happen **outside** any DB transaction.
* Each ``registry_raw_vacancies`` call wraps its three INSERTs in a
  single ``begin()`` for atomicity per vacancy.
* ``process_source`` commits after each keyword so progress is visible
  to the dashboard and the connection is released between HTTP calls.
"""

import logging
import traceback
from datetime import datetime
from typing import TYPE_CHECKING, Any
from zoneinfo import ZoneInfo

from src.core.database.types import StatusEventType
from src.modules.discovery_vacancy.infrastructure.models import (
    StatusRawVacancyType,
)
from src.modules.discovery_vacancy.infrastructure.repositories import (
    DiscoverySessionRepository,
)
from src.plugins.base import RawVacancy
from src.plugins.exceptions import BasePluginError

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

    from src.modules.analyze_vacancy.application.queue_analyze_service import (
        QueueAnalyzeService,
    )
    from src.modules.matching_vacancy.application.queue_matching_service import (
        QueueMatchingService,
    )
    from src.modules.resumes.application.services import ResumesService
    from src.modules.sources.application.services import SourcesService
    from src.plugins import (
        RawVacancy,
        RawVacancyFromFilter,
        SourcePluginRegistry,
    )

    from .raw_vacancy_service import RawVacancyService


log = logging.getLogger(__name__)


class DiscoveryService:
    """Orchestrates vacancy discovery and raw vacancy download."""

    def __init__(
        self,
        db_session: AsyncSession,
        plugin_registry: SourcePluginRegistry,
        sources_service: SourcesService,
        resumes_service: ResumesService,
        raw_vacancy_service: RawVacancyService,
        queue_matching_service: QueueMatchingService,
        queue_analyze_service: QueueAnalyzeService,
    ) -> None:
        """Initialize service.

        Args:
            db_session: Async SQLAlchemy session bound to this
                service. All DB operations go through it.
            plugin_registry: Registry of source plugins by code.
            sources_service: Access to source records.
            resumes_service: Access to resumes and keyword filters.
            raw_vacancy_service: Persistence for raw vacancies.
            queue_matching_service: Enqueue vacancies for matching.
            queue_analyze_service: Enqueue vacancies for analysis.
        """
        self._db_session = db_session
        self._sources_service = sources_service
        self._resumes_service = resumes_service
        self._raw_vacancy_service = raw_vacancy_service
        self._queue_matching_service = queue_matching_service
        self._queue_analyze_service = queue_analyze_service

        self._plugin_registry = plugin_registry

        self._repo_discovery_session = DiscoverySessionRepository(db_session)

    async def _start_discovery_session(
        self,
        source_id: int,
    ) -> int:
        """Create a discovery session and flush it to get an id.

        Flush is used instead of commit so the caller controls the
        transaction boundary.

        Args:
            source_id: Source the session belongs to.

        Returns:
            Newly created discovery session id.
        """
        session_obj = await self._repo_discovery_session.create(
            source_id=source_id,
            started_at=datetime.now(tz=ZoneInfo("UTC")),
        )
        await self._db_session.flush()

        log.info(
            "Discovery session started, id: %s, source_id: %s",
            session_obj.id,
            source_id,
        )
        return session_obj.id

    async def _update_state_discovery_session(
        self,
        session_id: int,
        payload: dict[str, Any],
    ) -> None:
        """Update discovery session fields without committing.

        Args:
            session_id: Discovery session id.
            payload: Column-value pairs to update.
        """
        await self._repo_discovery_session.update(session_id=session_id, **payload)

        log.debug(
            "Discovery session updated, id: %s, fields: %s",
            session_id,
            list(payload.keys()),
        )

    async def _close_discovery_session(
        self,
        session_id: int,
    ) -> None:
        """Mark discovery session as ``FINISHED``.

        Does not commit; the caller decides when to commit.

        Args:
            session_id: Discovery session id.
        """
        payload = {
            "finished_at": datetime.now(tz=ZoneInfo("UTC")),
            "status": StatusEventType.FINISHED,
        }
        await self._repo_discovery_session.update(session_id=session_id, **payload)

        log.info("Discovery session closed, id: %s", session_id)

    async def registry_error_discovery_session(
        self,
        source_id: int,
        error: Exception,
    ) -> None:
        """Mark discovery session as ``ERROR`` and store the error.

        Runs in a single transaction (``begin()``) so the status
        update and the error row are atomic. If no active session
        exists for the source, a new one is created.

        Expected to be called from a **fresh** session: the caller's
        previous session may have been rolled back.

        Args:
            source_id: Source id.
            error: Exception that caused the failure.
        """
        error_message = f"{type(error).__name__}: {error!s}"
        full_traceback = "".join(
            traceback.format_exception(type(error), error, error.__traceback__)
        )

        async with self._db_session.begin():
            discovery_session = await self._repo_discovery_session.get_by_source_id(
                source_id=source_id
            )

            if discovery_session is None:
                discovery_session_id = await self._start_discovery_session(
                    source_id=source_id
                )
                log.warning(
                    "No active discovery session for source_id: %s, "
                    "created new one, id: %s",
                    source_id,
                    discovery_session_id,
                )
            else:
                discovery_session_id = discovery_session.id

            await self._repo_discovery_session.update(
                session_id=discovery_session_id,
                status=StatusEventType.ERROR,
                finished_at=datetime.now(tz=ZoneInfo("UTC")),
            )
            await self._repo_discovery_session.add_error(
                session_id=discovery_session_id,
                error_message=error_message,
                traceback=full_traceback,
            )

        log.error(
            "Discovery session marked as ERROR, id: %s, source_id: %s, error_type: %s",
            discovery_session_id,
            source_id,
            type(error).__name__,
        )

    def _discover_for_source(
        self,
        source_type: str,
        keyword: str,
    ) -> list[RawVacancyFromFilter]:
        """Call the source plugin to fetch vacancies for a keyword.

        This performs a synchronous HTTP call, so it must be called
        outside any DB transaction.

        Args:
            source_type: Source code used to look up the plugin.
            keyword: Search keyword.

        Returns:
            List of vacancies returned by the plugin.
        """
        log.info(
            "Discovering vacancies, source: %s, keyword: %s",
            source_type,
            keyword,
        )

        vacancies = self._plugin_registry.get(source_type).discover(keyword=keyword)

        log.info(
            "Discovered %s vacancies, source: %s, keyword: %s",
            len(vacancies),
            source_type,
            keyword,
        )
        return vacancies

    async def process_source(
        self,
        source_id: int,
        source_code: str,
    ) -> tuple[int, str]:
        """Run discovery for a single source.

        Flow:

        1. Start a discovery session (flush, no commit).
        2. Load keywords and their resume ids.
        3. Mark the session as ``PROCESSING`` and commit.
        4. For each keyword: HTTP fetch, register vacancies,
           update counters, commit.
        5. Close the session and commit.

        HTTP happens between commits, so it is never inside an open
        transaction.

        Args:
            source_id: Source id.
            source_code: Source code used to look up the plugin.

        Returns:
            Tuple of ``(total_vacancies, session_args)``.
        """
        log.info(
            "Processing source start, source_id: %s, source_code: %s",
            source_id,
            source_code,
        )

        count_vacancies_by_source = 0
        discovery_session_id = await self._start_discovery_session(source_id=source_id)

        # Getting resumes by source
        keyword_to_resumes = await self._resumes_service.get_resumes_ids_by_source_id(
            source_id=source_id
        )

        log.info(
            "Loaded keywords for source, source_id: %s, keywords: %s",
            source_id,
            list(keyword_to_resumes.keys()),
        )

        session_args = str(keyword_to_resumes.items())
        payload = {
            "status": StatusEventType.PROCESSING,
            "vacancies_found": 0,
            "session_args": session_args,
        }
        await self._update_state_discovery_session(
            session_id=discovery_session_id,
            payload=payload,
        )
        await self._db_session.commit()

        for keyword, resume_ids in keyword_to_resumes.items():
            log.info(
                "Processing keyword, source_id: %s, keyword: %s, resume_count: %s",
                source_id,
                keyword,
                len(resume_ids),
            )

            vacancies_from_source_by_keyword = self._discover_for_source(
                source_type=str(source_code),
                keyword=keyword,
            )
            count_vacancies_by_keyword = len(vacancies_from_source_by_keyword)

            log.info(
                "Found %s vacancies, source_id: %s, keyword: %s",
                count_vacancies_by_keyword,
                source_id,
                keyword,
            )

            count_vacancies_by_source += count_vacancies_by_keyword

            await self.registry_raw_vacancies(
                session_id=discovery_session_id,
                source_id=source_id,
                resume_ids=resume_ids,
                vacancies_from_filter=vacancies_from_source_by_keyword,
                keyword=keyword,
            )

            payload = {
                "vacancies_found": count_vacancies_by_source,
            }
            await self._update_state_discovery_session(
                session_id=discovery_session_id,
                payload=payload,
            )
            await self._db_session.commit()

        await self._close_discovery_session(session_id=discovery_session_id)
        await self._db_session.commit()

        log.info(
            "Processing source finished, source_id: %s, total_vacancies: %s",
            source_id,
            count_vacancies_by_source,
        )
        return count_vacancies_by_source, session_args

    async def registry_raw_vacancies(
        self,
        session_id: int,
        source_id: int,
        resume_ids: list[int],
        vacancies_from_filter: list[RawVacancyFromFilter],
        keyword: str,
    ) -> None:
        """Persist vacancies and enqueue them for further processing.

        Each vacancy is written in its own transaction so that three
        INSERTs (raw vacancy, matching queue, analyze queue) are
        atomic per vacancy. A failure on one vacancy does not roll
        back already-registered vacancies.

        The caller must ensure the session is **not** already inside
        a transaction; otherwise ``begin()`` raises
        ``InvalidRequestError``.

        Args:
            session_id: Discovery session id to attach vacancies to.
            source_id: Source id.
            resume_ids: Resume ids to enqueue for matching.
            vacancies_from_filter: Vacancies returned by the plugin.
            keyword: Search keyword.
        """
        log.info(
            "Registering %s vacancies, source_id: %s, keyword: %s",
            len(vacancies_from_filter),
            source_id,
            keyword,
        )

        for vacancy_filter in vacancies_from_filter:
            async with self._db_session.begin():
                raw_vacancy = await (
                    self._raw_vacancy_service.register_discovered_vacancy(
                        session_id=session_id,
                        source_id=source_id,
                        url=vacancy_filter.url,
                        job_title=vacancy_filter.title,
                    )
                )
                log.info(
                    "Raw vacancy registered, id: %s, url: %s",
                    raw_vacancy.id,
                    vacancy_filter.url,
                )

                await self._queue_matching_service.add_many_vacancy_to_queue(
                    raw_vacancy_id=raw_vacancy.id,
                    resume_ids=resume_ids,
                    keyword=keyword,
                )
                log.debug(
                    "Queue matching added, raw_vacancy_id: %s, resume_count: %s",
                    raw_vacancy.id,
                    len(resume_ids),
                )

                await self._queue_analyze_service.add_vacancy_to_queue(
                    vacancy_id=raw_vacancy.id,
                    keyword=keyword,
                )
                log.debug(
                    "Queue analyze added, raw_vacancy_id: %s",
                    raw_vacancy.id,
                )

        log.info(
            "Registered %s vacancies, source_id: %s, keyword: %s",
            len(vacancies_from_filter),
            source_id,
            keyword,
        )

    async def get_vacancies_ids(
        self,
        limit: int = 100,
    ) -> list[int]:
        """Return ids of raw vacancies pending download.

        Args:
            limit: Maximum number of ids to return.

        Returns:
            List of raw vacancy ids in ``NOT_DOWNLOADED`` state.
        """
        vacancies = await self._raw_vacancy_service.get_download_pending_vacancies(
            status=StatusRawVacancyType.NOT_DOWNLOADED,
            limit=limit,
        )

        log.info(
            "Found %s vacancies to download, limit: %s",
            len(vacancies),
            limit,
        )
        return [v.id for v in vacancies]

    async def download_raw_vacancy(self, raw_vacancy_id: int) -> None:
        """Download one raw vacancy and persist its content.

        Flow:

        1. Read vacancy and source in a short transaction, keep
           primitive fields (id, url, source code).
        2. Call the plugin **outside** any transaction.
        3. Persist the result (or the error) in a second short
           transaction.

        ``BasePluginError`` is captured, persisted with
        ``status=ERROR``, and re-raised so the caller (Celery task)
        can decide what to do with it.

        Args:
            raw_vacancy_id: Raw vacancy id to download.

        Raises:
            ValueError: If vacancy or source is not found.
            BasePluginError: If the plugin failed to download.
        """
        async with self._db_session.begin():
            vacancy = await self._raw_vacancy_service.get_by_id(
                vacancy_id=raw_vacancy_id
            )

            if vacancy is None:
                log.warning("Raw vacancy not found, id: %s", raw_vacancy_id)
                raise ValueError(f"Raw vacancy not found, id: {raw_vacancy_id}")

            source = await self._sources_service.get_by_id(source_id=vacancy.source_id)
            if source is None:
                log.warning(
                    "Source not found, source_id: %s, vacancy_id: %s",
                    vacancy.source_id,
                    raw_vacancy_id,
                )
                raise ValueError(f"Source not found, id: {vacancy.source_id}")

            vacancy_id = vacancy.id
            vacancy_url = vacancy.url
            source_code = source.code

        log.info(
            "Downloading raw vacancy, id: %s, source: %s, url: %s",
            vacancy_id,
            source_code,
            vacancy_url,
        )

        plugin_error: BasePluginError | None = None
        try:
            downloaded_vacancy: RawVacancy = self._plugin_registry.get(
                source_type=source_code
            ).get_vacancy(
                url=vacancy_url,
            )

        except BasePluginError as e:
            plugin_error = e

            log.warning(
                "Plugin error on download, vacancy_id: %s, error_type: %s, error: %s",
                vacancy_id,
                type(e).__name__,
                e,
            )

            error_message = f"Text error: {e!s}"
            error_traceback = traceback.format_exc()
            errored_at = datetime.now(tz=ZoneInfo("UTC"))

            payload = {
                "error_message": error_message,
                "error_traceback": error_traceback,
                "error_type": type(e).__name__,
                "errored_at": errored_at,
                "status": StatusRawVacancyType.ERROR,
            }
        else:
            log.info(
                "Vacancy downloaded, id: %s, html_size: %s",
                vacancy_id,
                len(downloaded_vacancy.html_content or ""),
            )

            payload = {
                "html_content": downloaded_vacancy.html_content,
                "description": downloaded_vacancy.description,
                "body": downloaded_vacancy.body,
                "status": StatusRawVacancyType.DOWNLOADED,
            }

        async with self._db_session.begin():
            await self._raw_vacancy_service.update_vacancy(
                vacancy_id=vacancy_id,
                payload=payload,
            )

        if plugin_error is not None:
            raise plugin_error
