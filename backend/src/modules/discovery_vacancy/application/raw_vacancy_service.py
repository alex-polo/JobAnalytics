from typing import TYPE_CHECKING, Any

from src.modules.discovery_vacancy.infrastructure.repositories import (
    RawVacancyRepository,
)

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

    from src.modules.discovery_vacancy.infrastructure.models import (
        RawVacancyORM,
        StatusRawVacancyType,
    )


class RawVacancyService:
    """Service for discovering vacancies."""

    def __init__(
        self,
        session: AsyncSession,
    ) -> None:
        """Initialize service."""
        self._session = session
        self._raw_vacancy_repository = RawVacancyRepository(session)

    async def register_discovered_vacancy(
        self,
        session_id: int,
        source_id: int,
        url: str,
        job_title: str,
    ) -> RawVacancyORM:
        """Register discovered vacancy into database."""
        raw_vacancy = await self._raw_vacancy_repository.add_or_get_vacancy(
            session_id=session_id,
            source_id=source_id,
            url=url,
            job_title=job_title,
        )

        return raw_vacancy

    async def get_download_pending_vacancies(
        self,
        status: StatusRawVacancyType,
        limit: int,
    ) -> list[RawVacancyORM]:
        """Get raw vacancies by status and source id."""
        return await self._raw_vacancy_repository.get_by_status(
            status=status,
            limit=limit,
        )

    async def get_by_id(self, vacancy_id: int) -> RawVacancyORM:
        """Get raw vacancy by id."""
        vacancy = await self._raw_vacancy_repository.get_by_id(
            vacancy_id=vacancy_id,
        )

        if vacancy is None:
            raise ValueError(f"Raw vacancy not found, id: {vacancy_id}")

        return vacancy

    async def update_vacancy(self, vacancy_id: int, payload: dict[str, Any]) -> None:
        """Update raw vacancy."""
        await self._raw_vacancy_repository.update_vacancy(
            vacancy_id=vacancy_id,
            payload=payload,
        )
