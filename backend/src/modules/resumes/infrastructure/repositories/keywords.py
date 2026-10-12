from typing import TYPE_CHECKING

from sqlalchemy import select

from src.modules.resumes.infrastructure.models import KeywordsResumeORM

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


class ResumeKeywordsRepository:
    """Resumes repository."""

    def __init__(self, session: AsyncSession) -> None:
        """Init repository."""
        self._session = session

    async def get_keywords_by_resume_id(self, resume_id: int) -> list[str]:
        """Get resumes by keyword."""
        result = await self._session.execute(
            select(KeywordsResumeORM.keyword).where(
                KeywordsResumeORM.resume_id == resume_id
            )
        )
        return list(result.scalars().all())
