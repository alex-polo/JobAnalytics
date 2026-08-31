from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from types import TracebackType

    from src.users.domain.entities import RoleEntity, UserEntity


class IEmailService(ABC):
    """Email service interface."""

    @abstractmethod
    async def send_email(self, to: str, subject: str, body: str) -> None:
        """Sends an email."""
        raise NotImplementedError


class IUserRepository(ABC):
    """User repository interface."""

    @abstractmethod
    async def get_by_email(self, email: str) -> UserEntity | None:
        """Retrieve a user by email with preloaded roles.

        Uses joinedload to fetch roles and profile
        """
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, id: int) -> UserEntity | None:
        """Retrieve a user by id."""
        raise NotImplementedError

    @abstractmethod
    async def sync_user_exists(self, user: UserEntity) -> int:
        """Ensures that a user exists in the database."""
        raise NotImplementedError

    @abstractmethod
    async def sync_user_role_assignments(self, user_id: int, role_id: int) -> int:
        """Ensures that a user has a  role."""
        raise NotImplementedError


class IRoleRepository(ABC):
    """Role repository interface."""

    @abstractmethod
    async def sync_role_exists(self, role: RoleEntity) -> int:
        """Ensures that a role exists in the database."""
        raise NotImplementedError


class IUserUnitOfWork(ABC):
    """Unit of Work interface."""

    users: IUserRepository
    roles: IRoleRepository

    async def __aenter__(self) -> IUserUnitOfWork:
        """Enters the asynchronous runtime context.

        Returns:
            The Unit of Work instance itself.
        """
        return self

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
        await self.rollback()

    @abstractmethod
    async def commit(self) -> None:
        """Commits all changes made within the transaction.

        Raises:
            NotImplementedError: If the subclass does not implement
                this method.
        """
        raise NotImplementedError

    @abstractmethod
    async def rollback(self) -> None:
        """Rolls back all changes made within the transaction.

        Raises:
            NotImplementedError: If the subclass does not implement
                this method.
        """
        raise NotImplementedError
