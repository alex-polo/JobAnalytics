from typing import TYPE_CHECKING

from sqlalchemy.dialects.postgresql import insert

from src.core.database.types import StatusEventType
from src.modules.matching_vacancy.infrastructure.models import QueueMatchingORM

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


class QueueMatchingRepository:
    """Queue matching repository."""

    def __init__(self, session: AsyncSession) -> None:
        """Init repository."""
        self._session = session

    async def add(
        self,
        resume_id: int,
        raw_vacancy_id: int,
        keyword: str,
    ) -> None:
        """Add to queue."""
        queue_matching = QueueMatchingORM(
            resume_id=resume_id,
            raw_vacancy_id=raw_vacancy_id,
            keyword=keyword,
            status=StatusEventType.PENDING,
        )
        self._session.add(queue_matching)

    async def add_many(
        self,
        raw_vacancy_id: int,
        resume_ids: list[int],
        keyword: str,
    ) -> None:
        """Add many to queue."""
        insert_data = [
            {
                "vacancy_id": raw_vacancy_id,
                "resume_id": resume_id,
                "keyword": keyword,
                "status": StatusEventType.PENDING,
            }
            for resume_id in resume_ids
        ]
        stmt = insert(QueueMatchingORM).values(insert_data)
        stmt = stmt.on_conflict_do_nothing(
            index_elements=[
                "vacancy_id",
                "resume_id",
            ]
        )
        await self._session.execute(stmt)
