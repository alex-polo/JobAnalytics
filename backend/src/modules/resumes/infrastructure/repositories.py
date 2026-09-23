from typing import TYPE_CHECKING

from sqlalchemy import select
from sqlalchemy.orm import joinedload

from src.modules.resumes.infrastructure.models import ResumeORM

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


class ResumesRepository:
    """Resumes repository."""

    def __init__(self, session: AsyncSession) -> None:
        """Init repository."""
        self._session = session

    async def get_all(self) -> list[ResumeORM]:
        """Get all resumes with keywords and sources."""
        result = await self._session.execute(
            select(ResumeORM).options(
                joinedload(ResumeORM.keywords),
                joinedload(ResumeORM.sources),
            )
        )

        return list(result.scalars().unique().all())

    async def get_by_id(self, id: int) -> ResumeORM | None:
        """Get resume by id."""
        result = await self._session.execute(
            select(ResumeORM).where(ResumeORM.id == id)
        )
        return result.scalar_one_or_none()

    async def create(self, resume: ResumeORM) -> ResumeORM:
        """Create resume."""
        self._session.add(resume)
        await self._session.commit()
        return resume
