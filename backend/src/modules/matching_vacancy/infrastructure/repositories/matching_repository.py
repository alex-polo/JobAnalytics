from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


class MatchingRepository:
    """Queue matching repository."""

    def __init__(self, session: AsyncSession) -> None:
        """Init repository."""
        self._session = session

    async def add(
        self,
        resume_id: int,
        raw_vacancy_id: int,
        keyword: str,
    ) -> None:
        """Add matching to queue."""
        ...
