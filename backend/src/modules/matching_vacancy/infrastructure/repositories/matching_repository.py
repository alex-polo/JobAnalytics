from typing import TYPE_CHECKING, Any

from sqlalchemy import or_, select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import joinedload

from src.modules.discovery_vacancy.infrastructure.models import RawVacancyORM
from src.modules.matching_vacancy.infrastructure.models import ResumeMatchResultORM
from src.modules.resumes.infrastructure.models import ResumeORM

if TYPE_CHECKING:
    from datetime import datetime

    from sqlalchemy.ext.asyncio import AsyncSession

    from src.modules.matching_vacancy.domain.schemas import LocationItems, MatchLevel


class MatchingRepository:
    """Queue matching repository."""

    def __init__(self, session: AsyncSession) -> None:
        """Init repository."""
        self._session = session

    async def get_by_id(self, id: int) -> ResumeMatchResultORM | None:
        """Get resume match result by id."""
        stmt = select(ResumeMatchResultORM).where(ResumeMatchResultORM.id == id)
        return (await self._session.execute(stmt)).scalars().one_or_none()

    async def upsert(self, values: dict[str, Any]) -> None:
        """Insert or update resume match result."""
        stmt = (
            insert(ResumeMatchResultORM)
            .values(**values)
            .on_conflict_do_update(
                constraint="uq_match_result_resume_vacancy",
                set_={
                    k: v
                    for k, v in values.items()
                    if k not in ("resume_id", "vacancy_id")
                },
            )
        )
        await self._session.execute(stmt)

    async def get_list_item(
        self,
        q: str | None = None,
        match_level: MatchLevel | None = None,
        location: LocationItems | None = None,
        since: datetime | None = None,
    ) -> list[ResumeMatchResultORM]:
        """Get all matchings."""
        stmt = select(ResumeMatchResultORM).options(
            joinedload(ResumeMatchResultORM.vacancy),
            joinedload(ResumeMatchResultORM.resume),
        )

        if match_level:
            stmt = stmt.where(ResumeMatchResultORM.match_level == match_level)

        if location:
            stmt = stmt.where(ResumeMatchResultORM.location == location)

        if since:
            stmt = stmt.where(ResumeMatchResultORM.created_at >= since)

        if q:
            stmt = stmt.join(ResumeMatchResultORM.vacancy).join(
                ResumeMatchResultORM.resume
            )
            stmt = stmt.where(
                or_(
                    RawVacancyORM.job_title.ilike(f"%{q}%"),
                    ResumeORM.name.ilike(f"%{q}%"),
                )
            )

        result = await self._session.execute(stmt)
        return list(result.scalars().unique())
