import logging
import traceback
from datetime import UTC, datetime, timedelta
from typing import TYPE_CHECKING, Any
from zoneinfo import ZoneInfo

from src.modules.matching_vacancy.domain.entity import QueueMatchingClaimedItem
from src.modules.matching_vacancy.domain.schemas import (
    LocationItems,
    MatchLevel,
    ResumeMatchDetails,
    ResumeMatchInput,
    ResumeMatchListItem,
)

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

    from src.modules.discovery_vacancy.application.raw_vacancy_service import (
        RawVacancyService,
    )
    from src.modules.discovery_vacancy.infrastructure.models import RawVacancyORM
    from src.modules.matching_vacancy.domain.entity import QueueMatchingClaimedItem
    from src.modules.matching_vacancy.infrastructure.models import QueueMatchingORM
    from src.modules.matching_vacancy.infrastructure.repositories import (
        MatchingRepository,
    )
    from src.modules.resumes.application.services import ResumesService
    from src.modules.resumes.infrastructure.models import ResumeORM
    from src.plugins.llm.base import IAIPlugin

    from .queue_matching_service import (
        QueueMatchingService,
    )

log = logging.getLogger(__name__)


class MatchingService:
    """Matching service."""

    def __init__(
        self,
        db_session: AsyncSession,
        repo_matching: MatchingRepository,
        queue_matching_service: QueueMatchingService,
        raw_vacancy_service: RawVacancyService,
        resumes_service: ResumesService,
        ai_plugin: IAIPlugin,
    ) -> None:
        """Init."""
        self._db_session = db_session
        self._repo_matching = repo_matching
        self._queue_matching_service = queue_matching_service
        self._raw_vacancy_service: RawVacancyService = raw_vacancy_service
        self._raw_resume_service: ResumesService = resumes_service
        self._ai_plugin = ai_plugin

    async def queue_claim_batch(
        self, limit: int, options: dict[str, Any]
    ) -> list[QueueMatchingClaimedItem]:
        """Queue claim batch."""
        list_claimed: list[
            QueueMatchingClaimedItem
        ] = await self._queue_matching_service.claim_batch(
            limit=limit,
            options=options,
        )
        await self._db_session.commit()

        return list_claimed

    async def match(self, queue_id: int) -> None:
        """Match resume and vacancy."""
        queue_item: QueueMatchingORM = await self._queue_matching_service.get_by_id(
            queue_id=queue_id
        )

        vacancy: RawVacancyORM = await self._raw_vacancy_service.get_by_id(
            queue_item.vacancy_id
        )

        resume: ResumeORM = await self._raw_resume_service.get_by_id(
            queue_item.resume_id
        )

        response = await self._ai_plugin.execute(
            payload=ResumeMatchInput(
                resume_text=resume.text,
                vacancy_text=(
                    f"{vacancy.job_title}\n{vacancy.description}\n{vacancy.body}\n"
                ),
            )
        )

        log.info(
            "LLM match done queue_id=%s resume_id=%s vacancy_id=%s | ",
            queue_id,
            queue_item.resume_id,
            queue_item.vacancy_id,
        )

        matching_dict = response.data.model_dump()
        matching_dict["resume_id"] = queue_item.resume_id
        matching_dict["vacancy_id"] = queue_item.vacancy_id
        matching_dict["url"] = vacancy.url
        matching_dict["keyword"] = queue_item.keyword
        matching_dict["prompt_name"] = response.prompt_name
        matching_dict["prompt_version"] = response.prompt_version
        matching_dict["prompt_locale"] = response.prompt_locale
        matching_dict["model_name"] = response.model_name
        matching_dict["finish_reason"] = response.finish_reason
        matching_dict["input_tokens"] = response.input_tokens
        matching_dict["output_tokens"] = response.output_tokens
        matching_dict["total_tokens"] = response.total_tokens
        matching_dict["latency_ms"] = response.latency_ms

        await self._repo_matching.upsert(values=matching_dict)

        await self._db_session.commit()

    async def mark_done(self, queue_id: int) -> None:
        """Mark done."""
        await self._queue_matching_service.mark_done(queue_id=queue_id)
        await self._db_session.commit()

    async def mark_failed(
        self,
        queue_id: int,
        error: Exception,
    ) -> None:
        """Mark failed."""
        error_type = str(type(error))
        error_message = f"{type(error).__name__}: {error!s}"
        full_traceback = "".join(
            traceback.format_exception(
                type(error),
                error,
                error.__traceback__,
            )
        )
        finished_at = datetime.now(tz=ZoneInfo("UTC"))

        await self._db_session.rollback()

        await self._queue_matching_service.mark_failed(
            queue_id=queue_id,
            error_message=error_message,
            error_type=error_type,
            error_traceback=full_traceback,
            errored_at=finished_at,
        )
        await self._db_session.commit()

    async def get_matches_list(
        self,
        limit: int = 100,
        q: str | None = None,
        match_level: MatchLevel | None = None,
        location: LocationItems | None = None,
        date: str | None = None,
    ) -> list[ResumeMatchListItem]:
        """Get matches list."""
        if date and date != "all":
            days = int(date.rstrip("d"))
            since = datetime.now(UTC).replace(tzinfo=None) - timedelta(days=days)
        else:
            since = None

        matches_rows = await self._repo_matching.get_list_item(
            limit=limit,
            q=q,
            match_level=match_level,
            location=location,
            since=since,
        )

        return [
            ResumeMatchListItem(
                id=int(row.id),
                vacancy_title=row.vacancy.job_title,
                resume_title=row.resume.name,
                match_score=row.match_score,
                match_level=row.match_level,
                keyword=row.keyword,
                salary="N/A",
                location=row.location,
                location_match=row.location_match,
                url=row.url,
                created_at=row.created_at,
            )
            for row in matches_rows
        ]

    async def get_match_details(self, match_id: int) -> ResumeMatchDetails:
        """Get match details."""
        row = await self._repo_matching.get_by_id(match_id)

        return ResumeMatchDetails.model_validate(row)
