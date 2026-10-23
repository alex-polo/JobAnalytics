import traceback
from datetime import datetime
from typing import TYPE_CHECKING, Any
from zoneinfo import ZoneInfo

from src.modules.matching_vacancy.infrastructure.repositories import (
    MatchingRepository,
)

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

    from src.modules.discovery_vacancy.application.raw_vacancy_service import (
        RawVacancyService,
    )
    from src.modules.matching_vacancy.domain.entity import QueueMatchingClaimedItem
    from src.modules.resumes.application.services import ResumesService

    from .queue_matching_service import (
        QueueMatchingService,
    )


class MatchingService:
    """Matching service."""

    def __init__(
        self,
        db_session: AsyncSession,
        queue_matching_service: QueueMatchingService,
        raw_vacancy_service: RawVacancyService,
        resumes_service: ResumesService,
    ) -> None:
        """Init."""
        self._db_session = db_session
        self._repo_matching = MatchingRepository(db_session)
        self._queue_matching_service = queue_matching_service
        self._raw_vacancy_service: RawVacancyService = raw_vacancy_service
        self._raw_resume_service: ResumesService = resumes_service

    async def queue_claim_batch(self, limit: int) -> list[QueueMatchingClaimedItem]:
        """Queue claim batch."""
        list_claimed = await self._queue_matching_service.claim_batch(limit=limit)
        await self._db_session.commit()

        return list_claimed

    async def match(self, queue_id: int) -> dict[str, Any]:
        """Match resume and vacancy."""
        ...

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
