from typing import TYPE_CHECKING

from sqlalchemy import Select, select
from sqlalchemy.orm import joinedload, selectinload

from src.core.database.repository.sqlalchemy import SqlAlchemyBaseRepository
from src.users.application.interfaces import IRoleRepository, IUserRepository
from src.users.domain.entities import RoleEntity, UserEntity

from .models import AuthRoleORM, UserORM, UserRoleAssignmentORM

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


class UserRepository(
    SqlAlchemyBaseRepository[UserEntity, UserORM, int],
    IUserRepository,
):
    """User repository."""

    def __init__(self, session: AsyncSession) -> None:
        """Initialize the repository."""
        super().__init__(session, UserORM, UserEntity)

    def _get_base_user_query(self) -> Select[tuple[UserORM]]:

        return select(self._model_orm).options(
            joinedload(self._model_orm.profile),
            selectinload(self._model_orm.roles_assignments).selectinload(
                UserRoleAssignmentORM.role
            ),
        )

    async def get_by_email(self, email: str) -> UserEntity | None:
        """Retrieve a user by email with preloaded roles.

        Uses joinedload to fetch roles through the assignment table
        in a single SQL query.
        """
        result = await self._session.execute(
            self._get_base_user_query().filter_by(email=email)
        )

        obj = result.scalar_one_or_none()

        return self._to_domain(obj) if obj else None

    async def get_by_id(self, id: int) -> UserEntity | None:
        """Retrieve a user by id."""
        result = await self._session.execute(
            self._get_base_user_query().filter_by(id=id)
        )

        obj = result.scalar_one_or_none()

        return self._to_domain(obj) if obj else None

    async def sync_user_exists(self, user: UserEntity) -> int:
        """Ensures that a user exists in the database."""
        return await self.upsert(
            entity=user,
            index_elements=["email"],
        )

    async def sync_user_role_assignments(self, user_id: int, role_id: int) -> int:
        """Ensures that a user has a role."""
        from sqlalchemy.dialects.postgresql import insert as pg_insert

        from src.users.infrastructure.models import UserRoleAssignmentORM

        stmt = pg_insert(UserRoleAssignmentORM).values(
            user_id=user_id,
            role_id=role_id,
            source="system",
            reason="Initial root setup",
        )

        stmt = stmt.on_conflict_do_update(
            index_elements=["user_id", "role_id"],
            set_={"source": stmt.excluded.source, "reason": stmt.excluded.reason},
        )

        result = await self._session.execute(stmt.returning(UserRoleAssignmentORM.id))

        return result.scalar_one()


class RoleRepository(
    SqlAlchemyBaseRepository[RoleEntity, AuthRoleORM, int],
    IRoleRepository,
):
    """Role repository."""

    def __init__(self, session: AsyncSession) -> None:
        """Initialize the repository."""
        super().__init__(session, AuthRoleORM, RoleEntity)

    async def sync_role_exists(self, role: RoleEntity) -> int:
        """Ensures that a role exists in the database."""
        return await self.upsert(entity=role, index_elements=["name"])
