from typing import TYPE_CHECKING

from src.modules.resumes.infrastructure.repositories import ResumesRepository

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

    from src.modules.resumes.infrastructure.models import ResumeORM


class ResumesService:
    """Resume service."""

    def __init__(self, session: AsyncSession) -> None:
        """Init service."""
        self._session = session
        self._repo = ResumesRepository(session)

    async def get_all(self) -> list[ResumeORM]:
        """Get all resumes."""
        return await self._repo.get_all()
