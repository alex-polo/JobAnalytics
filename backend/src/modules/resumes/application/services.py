from typing import TYPE_CHECKING

from src.modules.resumes.infrastructure.repositories.keywords import (
    ResumeKeywordsRepository,
)
from src.modules.resumes.infrastructure.repositories.resumes import ResumesRepository

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

    from src.modules.resumes.infrastructure.models import ResumeORM


class ResumesService:
    """Resume service."""

    def __init__(self, session: AsyncSession) -> None:
        """Init service."""
        self._session = session
        self._resumes_repo = ResumesRepository(session)
        self.keywords_repo = ResumeKeywordsRepository(session)

    async def get_all(self) -> list[ResumeORM]:
        """Get all resumes."""
        return await self._resumes_repo.get_all()

    async def get_resumes_by_source(self, source_id: int) -> list[ResumeORM]:
        """Get resumes by source."""
        return await self._resumes_repo.get_resumes_by_source(source_id)

    async def get_resumes_ids_by_source_id(
        self,
        source_id: int,
    ) -> dict[str, list[int]]:
        """Get resumes ids by filter keywords for current source id."""
        resumes = await self._resumes_repo.get_resumes_by_source(source_id)

        # Getting keywords for resume by source
        keyword_to_resumes: dict[str, list[int]] = {}
        for resume in resumes:
            keywords = await self.keywords_repo.get_keywords_by_resume_id(resume.id)
            for keyword in keywords:
                if keyword not in keyword_to_resumes:
                    keyword_to_resumes[keyword] = []

                keyword_to_resumes[keyword].append(resume.id)

        return keyword_to_resumes

    async def get_resume_keywords(self, resume_id: int) -> list[str]:
        """Get resume keywords."""
        return await self.keywords_repo.get_keywords_by_resume_id(resume_id)

    async def get_by_id(self, resume_id: int) -> ResumeORM:
        """Get resume by id."""
        resume = await self._resumes_repo.get_by_id(resume_id)
        if resume is None:
            raise ValueError(f"Resume not found, resume_id: {resume_id}")

        return resume
