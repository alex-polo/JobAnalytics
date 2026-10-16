from typing import TYPE_CHECKING

from src.modules.analyze_vacancy.infrastructure.repositories import (
    QueueAnalyzeRepository,
)

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


class QueueAnalyzeService:
    """Service for queue matching."""

    def __init__(
        self,
        session: AsyncSession,
    ) -> None:
        """Init service."""
        self._session = session
        self._repo_analyze_matching = QueueAnalyzeRepository(session)

    async def add_vacancy_to_queue(self, vacancy_id: int, keyword: str) -> None:
        """Add vacancy to queue."""
        await self._repo_analyze_matching.add(
            raw_vacancy_id=vacancy_id,
            keyword=keyword,
        )

    async def add_many_vacancy_to_queue(
        self,
        raw_vacancy_id: list[int],
        keyword: str,
    ) -> None:
        """Add vacancy to queue."""
        await self._repo_analyze_matching.add_many(
            raw_vacancy_ids=raw_vacancy_id,
            keyword=keyword,
        )
