from typing import Annotated

from fastapi import Depends
from fastapi.security import (
    APIKeyCookie,
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm,
)

from src.auth.application.interfaces import ITokenProvider
from src.auth.application.service import AuthService
from src.auth.infrastructure.jwt import JwtRs256TokenProvider
from src.core.config import APP_SETTINGS
from src.core.security.deps import PasswordHasherDep  # noqa: TC001
from src.users.api.dependencies import UserUowDep  # noqa: TC001
from src.users.domain.entities import UserEntity

scheme_oauth2 = OAuth2PasswordBearer(
    tokenUrl=APP_SETTINGS.AUTH.token_url,
    auto_error=False,
)

scheme_cookie = APIKeyCookie(
    name=APP_SETTINGS.AUTH.cookie_name,
    auto_error=False,
)

FormDataDep = Annotated[OAuth2PasswordRequestForm, Depends(OAuth2PasswordRequestForm)]
RefreshTokenDep = Annotated[str | None, Depends(scheme_cookie)]


def get_token_provider() -> ITokenProvider:
    """Get token provider."""
    return JwtRs256TokenProvider(
        private_key=APP_SETTINGS.AUTH.private_key,
        public_key=APP_SETTINGS.AUTH.public_key,
        access_token_expire_minutes=APP_SETTINGS.AUTH.jwt_access_token_expire_minutes,
        refresh_token_expire_days=APP_SETTINGS.AUTH.jwt_refresh_token_expire_days,
    )


TokenProviderDep = Annotated[ITokenProvider, Depends(get_token_provider)]


def get_auth_service(
    uow: UserUowDep,
    hasher: PasswordHasherDep,
    token_provider: TokenProviderDep,
) -> AuthService:
    """Returns an AuthService instance."""
    return AuthService(
        uow=uow,
        hasher=hasher,
        token_provider=token_provider,
        auth_cfg=APP_SETTINGS.AUTH,
    )


AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]


async def get_current_user(
    token: Annotated[str, Depends(scheme_oauth2)],
    auth_service: AuthServiceDep,
) -> UserEntity:
    """Returns the current user."""
    return await auth_service.get_current_user(jwt_token=token)


CurrentUserDep = Annotated[UserEntity, Depends(get_current_user)]
