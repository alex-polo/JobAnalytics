from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.modules.sources.application.services import SourcesService


class SchedulerService:
    """Service for scheduling discovery tasks."""

    def __init__(self, sources_service: SourcesService) -> None:
        """Initialize service."""
        self.sources_service = sources_service

    async def get_sources_to_process(self) -> list[tuple[int, str]]:
        """Get sources to process."""
        return [
            (resource.id, resource.code)
            for resource in await self.sources_service.get_all_active()
        ]
