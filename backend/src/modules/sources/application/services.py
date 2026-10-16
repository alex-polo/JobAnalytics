from typing import TYPE_CHECKING

from src.modules.sources.infrastructure.repositories import SourcesRepository

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

    from src.modules.sources.infrastructure.models import SourceORM


class SourcesService:
    """Sources service."""

    def __init__(self, session: AsyncSession) -> None:
        """Constructor."""
        self._repository = SourcesRepository(session=session)

    async def get_all(self) -> list[SourceORM]:
        """Get all sources."""
        return await self._repository.get_all()

    async def get_all_active(self) -> list[SourceORM]:
        """Get all active sources."""
        return await self._repository.get_all_active()

    async def get_by_id(self, source_id: int) -> SourceORM | None:
        """Get source by id."""
        return await self._repository.get_by_id(source_id=source_id)
