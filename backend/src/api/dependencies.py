from typing import Annotated

from fastapi import Depends

from src.core.database.engine import DBSessionDep  # noqa: TC001
from src.modules.matching_vacancy.application.factory import MatchingServiceFactory
from src.modules.matching_vacancy.application.matching_service import MatchingService
from src.modules.resumes.application.services import ResumesService
from src.modules.sources.application.services import SourcesService


def get_sources_service(session: DBSessionDep) -> SourcesService:
    """Provide sources service."""
    return SourcesService(session)


def get_resumes_service(session: DBSessionDep) -> ResumesService:
    """Provide resumes service."""
    return ResumesService(session)


def get_resume_matching_service(session: DBSessionDep) -> MatchingService:
    """Provide resume matching service."""
    factory = MatchingServiceFactory(db_session=session)
    return factory.create_service()


# Если хочешь оставить алиасы для краткости, они должны выглядеть так:
SourcesServiceDep = Annotated[SourcesService, Depends(get_sources_service)]
ResumesServiceDep = Annotated[ResumesService, Depends(get_resumes_service)]
ResumeMatchingServiceDep = Annotated[
    MatchingService,
    Depends(get_resume_matching_service),
]
