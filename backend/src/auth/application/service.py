from typing import TYPE_CHECKING

from src.auth.domain.entities import CookieSettings, TokenEntity

from .exceptions import (
    AccountDisabledError,
    AccountNotVerifiedError,
    InvalidCredentialsError,
    InvalidTokenError,
    NoRolesAssignedError,
)

if TYPE_CHECKING:
    from src.auth.application.interfaces import ITokenProvider
    from src.core.config.classes import AuthSettings
    from src.core.security.interfaces import IPasswordHasher
    from src.users.application.interfaces import IUserUnitOfWork
    from src.users.domain.entities import UserEntity


class AuthService:
    """Service for managing auth-related business logic."""

    def __init__(
        self,
        uow: IUserUnitOfWork,
        hasher: IPasswordHasher,
        token_provider: ITokenProvider,
        auth_cfg: AuthSettings,
    ) -> None:
        """Initialize AuthService with dependencies."""
        self.uow = uow
        self.hasher = hasher
        self.token_provider = token_provider
        self.auth_cfg = auth_cfg

    def _ensure_valid_user(
        self,
        user: UserEntity | None,
    ) -> UserEntity:
        """Validate user is active and verified."""
        if not user or not user.id:
            raise InvalidCredentialsError()

        if not user.roles_assignments:
            raise NoRolesAssignedError()

        if not user.is_active:
            raise AccountDisabledError()

        if not user.is_verified:
            raise AccountNotVerifiedError()

        return user

    def _generate_tokens(
        self,
        user: UserEntity,
    ) -> TokenEntity:
        """Generate access and refresh tokens for user.

        Args:
            user: User entity to generate tokens for.

        Returns:
            TokenEntity containing access and refresh tokens.

        """
        access_token = self.token_provider.create_access_token(
            user_id=user.id,  # type: ignore
            roles=user.user_roles,
        )
        refresh_token = self.token_provider.create_refresh_token(user_id=user.id)  # type: ignore

        return self._create_jwt_token_pair(access_token, refresh_token)

    def _create_jwt_token_pair(
        self,
        access_token: str,
        refresh_token: str,
    ) -> TokenEntity:
        """Create token pair entity with cookie settings.

        Args:
            access_token: JWT access token string.
            refresh_token: JWT refresh token string.

        Returns:
            TokenEntity with tokens and cookie configuration.
        """
        return TokenEntity(
            access_token=access_token,
            refresh_token=refresh_token,
            cookie_settings=CookieSettings(
                name=self.auth_cfg.cookie_name,
                max_age=self.auth_cfg.cookie_max_age,
                path=self.auth_cfg.cookie_path,
                domain=self.auth_cfg.cookie_domain,
                secure=self.auth_cfg.cookie_secure,
                samesite=self.auth_cfg.cookie_samesite,
            ),
        )

    async def authenticate(
        self,
        username: str,
        password: str,
    ) -> TokenEntity:
        """Authenticate user with credentials and issue tokens.

        Args:
            username: User email or username.
            password: User password in plain text.

        Returns:
            TokenEntity with access and refresh tokens.

        Raises:
            InvalidCredentialsError: If credentials are invalid.
        """
        async with self.uow:
            user_from_db: UserEntity | None = await self.uow.users.get_by_email(
                email=username
            )
            if (
                not user_from_db
                or not user_from_db.id
                or not self.hasher.verify(password, user_from_db.hashed_password)
            ):
                raise InvalidCredentialsError()

            user: UserEntity = self._ensure_valid_user(user=user_from_db)

            return self._generate_tokens(user)

    async def refresh_session(
        self,
        refresh_token: str | None,
    ) -> TokenEntity:
        """Refresh session using refresh token.

        Args:
            refresh_token: JWT refresh token string.

        Returns:
            TokenEntity with new access and refresh tokens.

        Raises:
            InvalidTokenError: If token is missing or invalid.
            InvalidCredentialsError: If user not found.
        """
        if refresh_token is None:
            raise InvalidTokenError()

        user_payload = self.token_provider.decode_token(refresh_token)
        token_user_id = user_payload.get("sub")

        if (
            user_payload.get("token_type") != "refresh"
            or not token_user_id
            or not token_user_id.isdigit()
        ):
            raise InvalidTokenError()

        user_id = int(token_user_id)
        async with self.uow:
            user_from_db: UserEntity | None = await self.uow.users.get_by_id(id=user_id)

        user: UserEntity = self._ensure_valid_user(user=user_from_db)

        return self._generate_tokens(user)

    async def get_current_user(
        self,
        jwt_token: str,
    ) -> UserEntity:
        """Get authenticated user from JWT access token.

        Args:
            jwt_token: JWT access token string.

        Returns:
            UserEntity of authenticated user.

        Raises:
            InvalidTokenError: If token is invalid or wrong type.
            InvalidCredentialsError: If user not found.
        """
        user_payload = self.token_provider.decode_token(jwt_token)
        token_user_id = user_payload.get("sub")
        if (
            user_payload.get("token_type") != "access"
            or not token_user_id
            or not token_user_id.isdigit()
        ):
            raise InvalidTokenError()

        user_id = int(token_user_id)
        async with self.uow:
            user_from_db: UserEntity | None = await self.uow.users.get_by_id(id=user_id)

        return self._ensure_valid_user(user=user_from_db)

    async def logout(self) -> CookieSettings:
        """Create cookie settings for logout (invalidate cookies).

        Returns:
            CookieSettings with max_age=0 to clear auth cookies.
        """
        return CookieSettings(
            name=self.auth_cfg.cookie_name,
            max_age=0,
            path=self.auth_cfg.cookie_path,
            domain=self.auth_cfg.cookie_domain,
            secure=self.auth_cfg.cookie_secure,
            samesite=self.auth_cfg.cookie_samesite,
        )
