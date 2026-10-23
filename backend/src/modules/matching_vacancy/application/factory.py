from typing import TYPE_CHECKING

from src.modules.discovery_vacancy.application.raw_vacancy_service import (
    RawVacancyService,
)
from src.modules.resumes.application.services import ResumesService

from .matching_service import MatchingService
from .queue_matching_service import (
    QueueMatchingService,
)

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


class MatchingServiceFactory:
    """Factory for creating MatchingService instances."""

    def __init__(self, db_session: AsyncSession) -> None:
        """Initialize factory with database session."""
        self._db_session = db_session

    def create_service(self) -> MatchingService:
        """Create and return a DiscoveryService instance."""
        queue_matching_service = QueueMatchingService(session=self._db_session)
        resumes_service = ResumesService(session=self._db_session)
        raw_vacancy_service = RawVacancyService(session=self._db_session)

        return MatchingService(
            db_session=self._db_session,
            resumes_service=resumes_service,
            raw_vacancy_service=raw_vacancy_service,
            queue_matching_service=queue_matching_service,
        )
