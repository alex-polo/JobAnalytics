from typing import TYPE_CHECKING

from src.modules.matching_vacancy.infrastructure.repositories import (
    QueueMatchingRepository,
)

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


class QueueMatchingService:
    """Service for queue matching."""

    def __init__(
        self,
        session: AsyncSession,
    ) -> None:
        """Init service."""
        self._session = session
        self._repo_queue_matching = QueueMatchingRepository(session)

    async def add_many_vacancy_to_queue(
        self,
        resume_ids: list[int],
        raw_vacancy_id: int,
        keyword: str,
    ) -> None:
        """Add vacancy to queue."""
        await self._repo_queue_matching.add_many(
            resume_ids=resume_ids,
            raw_vacancy_id=raw_vacancy_id,
            keyword=keyword,
        )
