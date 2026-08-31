from fastapi import status

from src.core.exceptions.base import ApplicationError


class AuthError(ApplicationError):
    """Base exception for authentication failures."""

    def __init__(
        self,
        status_code: int = status.HTTP_401_UNAUTHORIZED,
        error_code: str = "ERR_AUTH",
    ) -> None:
        """Initialize exception."""
        super().__init__(status_code, self.message, error_code)

    message = "Authentication failed"


class InvalidCredentialsError(AuthError):
    """Raised when email or password is incorrect."""

    message = "Invalid email or password"


class AccountDisabledError(AuthError):
    """Raised when user account is disabled."""

    message = "Account is disabled"


class AccountNotVerifiedError(AuthError):
    """Raised when user account is not verified."""

    message = "Account is not verified"


class NoRolesAssignedError(AuthError):
    """Raised when user has no roles assigned."""

    message = "User has no roles assigned. Access denied."


class TokenExpiredError(AuthError):
    """Raised when authentication token has expired."""

    message = "Session expired, please login again"


class InvalidTokenError(AuthError):
    """Raised when token is malformed or invalid."""

    message = "Invalid token provided"
