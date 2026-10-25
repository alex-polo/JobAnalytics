from typing import TYPE_CHECKING, Any

from sqlalchemy.dialects.postgresql import insert

from src.modules.matching_vacancy.infrastructure.models import ResumeMatchResultORM

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


class MatchingRepository:
    """Queue matching repository."""

    def __init__(self, session: AsyncSession) -> None:
        """Init repository."""
        self._session = session

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
