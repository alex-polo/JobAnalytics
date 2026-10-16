from typing import TYPE_CHECKING, Any

from sqlalchemy import select, update

from src.modules.discovery_vacancy.infrastructure.models import (
    RawVacancyORM,
    StatusRawVacancyType,
)

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


class RawVacancyRepository:
    """Vacancy raw repository."""

    def __init__(self, session: AsyncSession) -> None:
        """Init repository."""
        self._session = session

    async def add_or_get_vacancy(
        self,
        session_id: int,
        source_id: int,
        url: str,
        job_title: str,
    ) -> RawVacancyORM:
        """Add or get vacancy."""
        vacancy_stmt = select(RawVacancyORM).where(
            RawVacancyORM.url == url,
            RawVacancyORM.job_title == job_title,
        )
        vacancy_result = await self._session.execute(vacancy_stmt)
        vacancy = vacancy_result.scalar_one_or_none()

        if vacancy is None:
            vacancy = RawVacancyORM(
                session_id=session_id,
                source_id=source_id,
                url=url,
                job_title=job_title,
                html_content=None,
                status=StatusRawVacancyType.NOT_DOWNLOADED,
            )
            self._session.add(vacancy)
            await self._session.flush()

        return vacancy

    async def get_by_status(
        self,
        status: StatusRawVacancyType,
        limit: int,
    ) -> list[RawVacancyORM]:
        """Get vacancies by status."""
        query = (
            select(RawVacancyORM)
            .where(
                RawVacancyORM.status == status,
            )
            .limit(limit)
        )
        vacancy_result = await self._session.execute(query)
        return list(vacancy_result.scalars().all())

    async def get_by_id(self, vacancy_id: int) -> RawVacancyORM | None:
        """Get vacancy by id."""
        result = await self._session.execute(
            select(RawVacancyORM).where(RawVacancyORM.id == vacancy_id)
        )
        return result.scalar_one_or_none()

    async def update_vacancy(self, vacancy_id: int, payload: dict[str, Any]) -> None:
        """Update vacancy."""
        await self._session.execute(
            update(RawVacancyORM)
            .where(RawVacancyORM.id == vacancy_id)
            .values(**payload)
        )
