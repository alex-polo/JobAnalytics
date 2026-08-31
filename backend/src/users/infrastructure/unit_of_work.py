from typing import TYPE_CHECKING

from src.users.application.interfaces import IUserUnitOfWork

from .repositories import RoleRepository, UserRepository

if TYPE_CHECKING:
    from types import TracebackType

    from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker


class UsersSqlAlchemyUnitOfWork(IUserUnitOfWork):
    """Unit of Work implementation for SQLAlchemy."""

    def __init__(self, session_factory: async_sessionmaker[AsyncSession]) -> None:
        """Initializes the Unit of Work with a Session Factory."""
        self._session_factory = session_factory

    async def __aenter__(self) -> IUserUnitOfWork:
        """Enters the asynchronous runtime context.

        Returns:
            The Unit of Work instance itself.
        """
        self._session: AsyncSession = self._session_factory()
        self.users = UserRepository(self._session)
        self.roles = RoleRepository(self._session)

        return await super().__aenter__()

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """Exits the asynchronous runtime context.

        Rolls back the transaction if an exception occurred.

        Args:
            exc_type: The type of the exception raised, if any.
            exc_val: The instance of the exception raised, if any.
            exc_tb: The traceback of the exception raised, if any.
        """
        await super().__aexit__(exc_type, exc_val, exc_tb)
        await self._session.close()

    async def commit(self) -> None:
        """Commits all changes made within the transaction."""
        await self._session.commit()

    async def rollback(self) -> None:
        """Rolls back all changes made within the transaction."""
        await self._session.rollback()
