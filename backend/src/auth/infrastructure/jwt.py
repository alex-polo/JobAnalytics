from datetime import UTC, datetime, timedelta
from typing import Any

import jwt

from src.auth.application.exceptions import InvalidTokenError, TokenExpiredError
from src.auth.application.interfaces import ITokenProvider


class JwtRs256TokenProvider(ITokenProvider):
    """RS256 JWT provider implementation using PEM certificates."""

    def __init__(
        self,
        private_key: str,
        public_key: str,
        access_token_expire_minutes: int = 30,
        refresh_token_expire_days: int = 30,
    ) -> None:
        """Initializes the JwtTokenProvider."""
        self.private_key = private_key
        self.public_key = public_key
        self.access_expire = access_token_expire_minutes
        self.refresh_expire = refresh_token_expire_days
        self.algorithm = "RS256"

    def create_access_token(self, user_id: int, roles: list[str]) -> str:
        """Creates a signed JWT using the private RSA key."""
        now = datetime.now(UTC)
        expiration = now + timedelta(minutes=self.access_expire)

        payload = {
            "token_type": "access",
            "sub": str(user_id),
            "roles": roles,
            "iat": now,
            "exp": expiration,
        }
        payload_encode: bytes = jwt.encode(
            payload,
            self.private_key,
            algorithm=self.algorithm,
        )

        return (
            payload_encode.decode("utf-8")
            if isinstance(payload_encode, bytes)
            else payload_encode
        )  # pyright: ignore[reportReturnType]

    def create_refresh_token(self, user_id: int) -> str:
        """Creates a signed JWT using the private RSA key."""
        now = datetime.now(UTC)
        expiration = now + timedelta(days=self.refresh_expire)

        payload = {
            "token_type": "refresh",
            "sub": str(user_id),
            "iat": now,
            "exp": expiration,
        }

        payload_encode: bytes = jwt.encode(
            payload,
            self.private_key,
            algorithm=self.algorithm,
        )

        return (
            payload_encode.decode("utf-8")
            if isinstance(payload_encode, bytes)
            else payload_encode
        )  # pyright: ignore[reportReturnType]

    def decode_token(self, token: str) -> dict[str, Any]:
        """Verifies the JWT using the public RSA key."""
        try:
            return jwt.decode(token, self.public_key, algorithms=[self.algorithm])
        except jwt.ExpiredSignatureError as e:
            raise TokenExpiredError() from e
        except jwt.PyJWTError as e:
            raise InvalidTokenError() from e
