from typing import TYPE_CHECKING

from fastapi import APIRouter, Response, status

from src.auth.api.dependencies import (  # noqa: TC001
    AuthServiceDep,
    FormDataDep,
    RefreshTokenDep,
)
from src.auth.api.schemas import BearerToken
from src.core.config.settings import APP_SETTINGS

if TYPE_CHECKING:
    from src.auth.domain.entities import TokenEntity

auth_router = APIRouter(prefix=APP_SETTINGS.AUTH.prefix, tags=["auth"])


@auth_router.post("/login", status_code=status.HTTP_200_OK)
async def login(
    response: Response,
    form_data: FormDataDep,
    auth_service: AuthServiceDep,
) -> BearerToken:
    """Handle user login."""
    token_data: TokenEntity = await auth_service.authenticate(
        username=form_data.username,
        password=form_data.password,
    )
    response.set_cookie(
        key=token_data.cookie_settings.name,
        value=token_data.refresh_token,
        httponly=True,
        **token_data.cookie_settings.model_dump(exclude={"name"}),
    )

    return BearerToken(access_token=token_data.access_token, token_type="bearer")  # noqa: S106


@auth_router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(
    auth_service: AuthServiceDep,
    response: Response,
) -> None:
    """Handle user logout."""
    cookie_settings = await auth_service.logout()
    response.set_cookie(
        key=cookie_settings.name,
        value="",
        httponly=True,
        **cookie_settings.model_dump(exclude={"name"}),
    )
    return


@auth_router.post("/refresh", status_code=status.HTTP_200_OK)
async def refresh(
    auth_service: AuthServiceDep,
    response: Response,
    refresh_token: RefreshTokenDep = None,
) -> BearerToken:
    """Handle token refresh."""
    token_data: TokenEntity = await auth_service.refresh_session(refresh_token)

    response.set_cookie(
        key=token_data.cookie_settings.name,
        value=token_data.refresh_token,
        httponly=True,
        **token_data.cookie_settings.model_dump(exclude={"name"}),
    )

    return BearerToken(
        access_token=token_data.access_token, token_type=token_data.token_type
    )
