from typing import Annotated

from fastapi import Depends

from src.core.database.engine import SessionFactoryDep  # noqa: TC001
from src.core.security.deps import PasswordHasherDep  # noqa: TC001
from src.users.application.interfaces import IUserUnitOfWork
from src.users.application.service import UserService
from src.users.infrastructure.unit_of_work import UsersSqlAlchemyUnitOfWork


def get_user_uow(
    async_session_factory: SessionFactoryDep,
) -> IUserUnitOfWork:
    """Returns a Unit of Work instance."""
    return UsersSqlAlchemyUnitOfWork(session_factory=async_session_factory)


UserUowDep = Annotated[IUserUnitOfWork, Depends(get_user_uow)]


def get_user_service(uow: UserUowDep, pass_hasher: PasswordHasherDep) -> UserService:
    """Returns a UserService instance."""
    return UserService(uow=uow, pass_hasher=pass_hasher)


user_service_deps = Annotated[UserService, Depends(get_user_service)]
