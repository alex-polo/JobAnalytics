from typing import TYPE_CHECKING

from sqlalchemy.dialects.postgresql import insert

from src.core.database.types import StatusEventType
from src.modules.analyze_vacancy.infrastructure.models import QueueAnalyzeVacancyORM

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


class QueueAnalyzeRepository:
    """Queue matching repository."""

    def __init__(self, session: AsyncSession) -> None:
        """Init repository."""
        self._session = session

    async def add(
        self,
        raw_vacancy_id: int,
        keyword: str,
    ) -> None:
        """Add to queue."""
        queue_analize = QueueAnalyzeVacancyORM(
            vacancy_id=raw_vacancy_id,
            keyword=keyword,
            status=StatusEventType.PENDING,
        )

        self._session.add(queue_analize)

    async def add_many(
        self,
        raw_vacancy_ids: list[int],
        keyword: str,
    ) -> None:
        """Add many to queue."""
        insert_data = [
            {
                "vacancy_id": raw_vacancy_id,
                "keyword": keyword,
                "status": StatusEventType.PENDING,
            }
            for raw_vacancy_id in raw_vacancy_ids
        ]
        stmt = insert(QueueAnalyzeVacancyORM).values(insert_data)
        stmt = stmt.on_conflict_do_nothing(
            index_elements=[
                "vacancy_id",
            ]
        )
        await self._session.execute(stmt)
