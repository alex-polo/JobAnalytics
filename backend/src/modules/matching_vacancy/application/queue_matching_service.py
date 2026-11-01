from typing import TYPE_CHECKING

from sqlalchemy import update

from src.core.database.types import StatusEventType
from src.modules.matching_vacancy.infrastructure.models import QueueMatchingORM
from src.modules.matching_vacancy.infrastructure.repositories import (
    QueueMatchingRepository,
)

if TYPE_CHECKING:
    from datetime import datetime

    from sqlalchemy.ext.asyncio import AsyncSession

    from src.modules.matching_vacancy.domain.entity import QueueMatchingClaimedItem


class QueueMatchingService:
    """Service for queue matching."""

    def __init__(
        self,
        session: AsyncSession,
    ) -> None:
        """Init service."""
        self._session = session
        self._repo_queue_matching = QueueMatchingRepository(session)

    async def get_by_id(self, queue_id: int) -> QueueMatchingORM:
        """Get queue item by id."""
        queue_item = await self._repo_queue_matching.get_by_id(id=queue_id)
        if queue_item is None:
            raise ValueError(f"Queue item not found, queue_id: {queue_id}")

        return queue_item

    async def add_many_vacancy_to_queue(
        self,
        resume_ids: list[int],
        raw_vacancy_id: int,
        keyword: str,
    ) -> None:
        """Add vacancy to queue."""
        await self._repo_queue_matching.add_many(
            resume_ids=resume_ids,
            vacancy_id=raw_vacancy_id,
            keyword=keyword,
        )

    async def claim_batch(self, limit: int) -> list[QueueMatchingClaimedItem]:
        """Claim batch."""
        return await self._repo_queue_matching.claim_batch(limit=limit)

    async def mark_done(self, queue_id: int) -> None:
        """PROCESSING -> DONE."""
        await self._repo_queue_matching.mark_done(queue_id=queue_id)

    async def mark_failed(
        self,
        queue_id: int,
        error_message: str,
        error_type: str,
        error_traceback: str,
        errored_at: datetime,
    ) -> None:
        """Mark queue item as failed with provided error details."""
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
