from typing import TYPE_CHECKING

from src.modules.analyze_vacancy.application.queue_analyze_service import (
    QueueAnalyzeService,
)
from src.modules.discovery_vacancy.application.raw_vacancy_service import (
    RawVacancyService,
)
from src.modules.matching_vacancy.application.queue_matching_service import (
    QueueMatchingService,
)
from src.modules.resumes.application.services import ResumesService
from src.modules.sources.application.services import SourcesService
from src.plugins.sources.registry import SourcePluginRegistry

from .discovery_service import DiscoveryService

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


class DiscoveryServiceFactory:
    """Factory for creating DiscoveryService instances."""

    def __init__(
        self,
        db_session: AsyncSession,
    ) -> None:
        """Initialize factory with database session."""
        self._db_session = db_session
        self._plugin_registry = SourcePluginRegistry.get_instance()

    def create_discovery_service(self) -> DiscoveryService:
        """Create and return a DiscoveryService instance."""
        sources_service = SourcesService(session=self._db_session)
        resumes_service = ResumesService(session=self._db_session)
        raw_vacancy_service = RawVacancyService(session=self._db_session)
        queue_matching_service = QueueMatchingService(session=self._db_session)
        queue_analyze_service = QueueAnalyzeService(session=self._db_session)

        return DiscoveryService(
            db_session=self._db_session,
            plugin_registry=self._plugin_registry,
            sources_service=sources_service,
            resumes_service=resumes_service,
            raw_vacancy_service=raw_vacancy_service,
            queue_matching_service=queue_matching_service,
            queue_analyze_service=queue_analyze_service,
        )
