from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


class SourcesService:
    """Sources service."""

    def __init__(self, session: AsyncSession) -> None:
        """Constructor."""
        self._session = session
