import logging
import traceback
from datetime import datetime
from typing import TYPE_CHECKING
from zoneinfo import ZoneInfo

from src.modules.matching_vacancy.domain.schemas import ResumeMatchInput

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
    from src.plugins.llm.base import IAIPlugin, LLMResponse

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

    async def queue_claim_batch(self, limit: int) -> list[QueueMatchingClaimedItem]:
        """Queue claim batch."""
        list_claimed = await self._queue_matching_service.claim_batch(limit=limit)
        await self._db_session.commit()

        return list_claimed

    async def match(self, queue_id: int) -> None:
        """Match resume and vacancy."""
        queue_item: QueueMatchingORM = await self._queue_matching_service.get_by_id(
            queue_id=queue_id
        )
        resume: ResumeORM = await self._raw_resume_service.get_by_id(
            queue_item.resume_id
        )
        vacancy: RawVacancyORM = await self._raw_vacancy_service.get_by_id(
            queue_item.vacancy_id
        )

        response: LLMResponse = await self._ai_plugin.execute(
            payload=ResumeMatchInput(
                resume_text=resume.text,
                vacancy_text=(
                    f"{vacancy.job_title}\n{vacancy.description}\n{vacancy.body}\n"
                ),
            )
        )

        log.info(
            "LLM match done queue_id=%s resume_id=%s vacancy_id=%s | "
            "prompt=%s v%s (%s) model=%s finish=%s | "
            "tokens in=%s out=%s total=%s latency=%sms",
            queue_id,
            queue_item.resume_id,
            queue_item.vacancy_id,
            response.prompt_name,
            response.prompt_version,
            response.prompt_locale,
            response.model_name,
            response.finish_reason,
            response.input_tokens,
            response.output_tokens,
            response.total_tokens,
            response.latency_ms,
        )

        matching_dict = response.data.model_dump()
        matching_dict["resume_id"] = queue_item.resume_id
        matching_dict["vacancy_id"] = queue_item.vacancy_id
        matching_dict["url"] = vacancy.url
        matching_dict["keyword"] = queue_item.keyword

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
