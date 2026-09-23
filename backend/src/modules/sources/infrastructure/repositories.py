from typing import TYPE_CHECKING

from sqlalchemy import select

from .models import SourceORM

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


class SourcesRepository:
    """Sources repository."""

    def __init__(self, session: AsyncSession) -> None:
        """Constructor."""
        self._session = session

    async def get_all(self) -> list[SourceORM]:
        """Get all active sources."""
        result = await self._session.execute(select(SourceORM))
        return list(result.scalars().all())

    async def get_all_active(self) -> list[SourceORM]:
        """Get all active sources."""
        result = await self._session.execute(
            select(SourceORM).where(SourceORM.is_active)
        )
        return list(result.scalars().all())

    async def get_by_id(self, source_id: int) -> SourceORM | None:
        """Get source by id."""
        result = await self._session.execute(
            select(SourceORM).where(SourceORM.id == source_id)
        )
        return result.scalar_one_or_none()
