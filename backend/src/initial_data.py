import asyncio
import logging

from src.core.config.settings import APP_SETTINGS
from src.core.database import DB_HANDLER
from src.core.security import PasswordHasher
from src.users.api.schemas import (
    RoleCreateSchema,
    UserCreateSchema,
)
from src.users.application.service import UserService
from src.users.infrastructure.unit_of_work import UsersSqlAlchemyUnitOfWork

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


async def init() -> None:
    """Initialize database connection."""
    if not APP_SETTINGS.ROOT_USER.should_create:
        log.info("No root user creation required")
        return

    uow = UsersSqlAlchemyUnitOfWork(DB_HANDLER.async_session_maker)
    pass_hasher = PasswordHasher()
    user_service = UserService(uow, pass_hasher)

    root_user_data = UserCreateSchema(
        email=APP_SETTINGS.ROOT_USER.email,
        password=APP_SETTINGS.ROOT_USER.password.get_secret_value(),
        is_active=True,
        is_verified=True,
    )

    root_role_data = RoleCreateSchema(name="root", title="root users", is_active=True)

    await user_service.initialize_root_access(
        user_schema=root_user_data,
        role_schema=root_role_data,
    )


async def main() -> None:
    """Run before the server starts."""
    try:
        log.info("Creating initial data")
        await init()
        log.info("Initial data successfully ensured/created")
    except Exception as e:  # noqa: BLE001
        log.error(f"Initialization failed: {e}")
        exit(1)
    finally:
        await DB_HANDLER.dispose_engine()


if __name__ == "__main__":
    asyncio.run(main())
