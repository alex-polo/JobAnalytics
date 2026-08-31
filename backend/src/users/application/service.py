from typing import TYPE_CHECKING

from src.users.domain.entities import RoleEntity, UserEntity

if TYPE_CHECKING:
    from src.core.security.interfaces import IPasswordHasher
    from src.users.api.schemas import RoleCreateSchema, UserCreateSchema

    from .interfaces import IUserUnitOfWork


class UserService:
    """Service for managing user-related business logic.

    Attributes:
        uow: Unit of Work for atomic database operations.
    """

    def __init__(
        self,
        uow: IUserUnitOfWork,
        pass_hasher: IPasswordHasher,
        #  mailer: IEmailService  # noqa: ERA001
    ) -> None:
        """Initializes the UserService with a Unit of Work."""
        self.uow = uow
        self.pass_hasher = pass_hasher
        # self.mailer = mailer  # noqa: ERA001

    async def initialize_root_access(
        self,
        user_schema: UserCreateSchema,
        role_schema: RoleCreateSchema,
    ) -> None:
        """Initializes the root user with a default role."""
        hashed_pw: str = self.pass_hasher.hash(user_schema.password)

        user_to_save = UserEntity(
            **user_schema.model_dump(
                exclude={"password", "profile"},
                exclude_none=True,
            ),
            hashed_password=hashed_pw,
        )

        role_to_save = RoleEntity(**role_schema.model_dump())

        async with self.uow:
            user_id: int = await self.uow.users.sync_user_exists(user=user_to_save)
            role_id: int = await self.uow.roles.sync_role_exists(role=role_to_save)

            await self.uow.users.sync_user_role_assignments(
                user_id=user_id,
                role_id=role_id,
            )

            await self.uow.commit()
