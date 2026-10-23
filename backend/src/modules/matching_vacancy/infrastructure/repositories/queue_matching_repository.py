from typing import TYPE_CHECKING

from sqlalchemy import select, update
from sqlalchemy.dialects.postgresql import insert

from src.core.database.types import StatusEventType
from src.modules.discovery_vacancy.infrastructure.models import (
    RawVacancyORM,
    StatusRawVacancyType,
)
from src.modules.matching_vacancy.domain.entity import (
    QueueMatchingClaimedItem,
)
from src.modules.matching_vacancy.infrastructure.models import QueueMatchingORM

if TYPE_CHECKING:
    from datetime import datetime

    from sqlalchemy.ext.asyncio import AsyncSession


class QueueMatchingRepository:
    """Queue matching repository."""

    def __init__(self, session: AsyncSession) -> None:
        """Init repository."""
        self._session = session

    async def add(
        self,
        resume_id: int,
        vacancy_id: int,
        keyword: str,
    ) -> None:
        """Add to queue."""
        queue_matching = QueueMatchingORM(
            resume_id=resume_id,
            vacancy_id=vacancy_id,
            keyword=keyword,
            status=StatusEventType.PENDING,
        )
        self._session.add(queue_matching)

    async def add_many(
        self,
        vacancy_id: int,
        resume_ids: list[int],
        keyword: str,
    ) -> None:
        """Add many to queue."""
        insert_data = [
            {
                "vacancy_id": vacancy_id,
                "resume_id": resume_id,
                "keyword": keyword,
                "status": StatusEventType.PENDING,
                "attempts": 0,
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

    async def claim_batch(self, limit: int = 100) -> list[QueueMatchingClaimedItem]:
        """Атомарно PENDING -> RUNNING, вернуть захваченные записи."""
        sub_query = (
            select(QueueMatchingORM.id)
            .join(
                RawVacancyORM,
                RawVacancyORM.id == QueueMatchingORM.vacancy_id,
            )
            .where(
                QueueMatchingORM.status == StatusEventType.PENDING,
                RawVacancyORM.status == StatusRawVacancyType.DOWNLOADED,
            )
            .order_by(QueueMatchingORM.created_at)
            .limit(limit)
            .with_for_update(skip_locked=True, of=QueueMatchingORM)
        )

        stmt = (
            update(QueueMatchingORM)
            .where(QueueMatchingORM.id.in_(sub_query))
            .values(
                status=StatusEventType.PROCESSING,
                attempts=QueueMatchingORM.attempts + 1,
            )
            .returning(
                QueueMatchingORM.id,
                QueueMatchingORM.resume_id,
                QueueMatchingORM.vacancy_id,
                QueueMatchingORM.keyword,
                QueueMatchingORM.attempts,
            )
        )

        result = await self._session.execute(stmt)
        return [
            QueueMatchingClaimedItem(
                id=r.id,
                resume_id=r.resume_id,
                raw_vacancy_id=r.vacancy_id,
                vacancy_keyword=r.keyword,
                attempts=r.attempts,
            )
            for r in result
        ]

    async def mark_done(self, queue_id: int) -> None:
        """PROCESSING -> DONE."""
        stmt = (
            update(QueueMatchingORM)
            .where(
                QueueMatchingORM.id == queue_id,
                QueueMatchingORM.status == StatusEventType.PROCESSING,
            )
            .values(
                status=StatusEventType.DONE,
                error_message=None,
                error_type=None,
                error_traceback=None,
                errored_at=None,
            )
        )
        await self._session.execute(stmt)

    async def mark_failed(
        self,
        queue_id: int,
        error_message: str,
        error_type: str,
        error_traceback: str,
        errored_at: datetime,
    ) -> None:
        """PROCESSING -> FAILED."""
        stmt = (
            update(QueueMatchingORM)
            .where(
                QueueMatchingORM.id == queue_id,
                QueueMatchingORM.status == StatusEventType.PROCESSING,
            )
            .values(
                status=StatusEventType.FAILED,
                error_message=error_message,
                error_type=error_type,
                error_traceback=error_traceback,
                errored_at=errored_at,
            )
        )
        await self._session.execute(stmt)
