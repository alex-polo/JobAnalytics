from typing import TYPE_CHECKING, Any

from sqlalchemy import select, update

from src.core.database.types import StatusEventType
from src.modules.discovery_vacancy.infrastructure.models import (
    DiscoveryErrorORM,
    DiscoverySessionORM,
)

if TYPE_CHECKING:
    from datetime import datetime

    from sqlalchemy.ext.asyncio import AsyncSession


class DiscoverySessionRepository:
    """Repository for discovery session."""

    def __init__(self, session: AsyncSession) -> None:
        """Init repository."""
        self._session = session

    async def get_by_source_id(self, source_id: int) -> DiscoverySessionORM | None:
        """Get discovery session by id."""
        query = select(DiscoverySessionORM).where(
            DiscoverySessionORM.source_id == source_id
        )
        discovery_session = await self._session.execute(query)

        return discovery_session.scalar_one_or_none()

    async def create(
        self,
        source_id: int,
        started_at: datetime,
    ) -> DiscoverySessionORM:
        """Create discovery session."""
        discovery_session = DiscoverySessionORM(
            source_id=source_id,
            started_at=started_at,
            finished_at=None,
            status=StatusEventType.STARTED,
            vacancies_found=0,
        )
        self._session.add(discovery_session)
        await self._session.flush()

        return discovery_session

    async def update(self, session_id: int, **payload: Any) -> None:  # noqa: ANN401
        """Update discovery session."""
        query = (
            update(DiscoverySessionORM)
            .where(DiscoverySessionORM.id == session_id)
            .values(**payload)
            .execution_options(synchronize_session="fetch")
        )
        await self._session.execute(query)

    async def add_error(
        self,
        session_id: int,
        error_message: str,
        traceback: str,
    ) -> None:
        """Добавить запись об ошибке в сессию обхода."""
        error_entry = DiscoveryErrorORM(
            session_id=session_id,
            error_message=error_message,
            traceback=traceback,
        )
        self._session.add(error_entry)
