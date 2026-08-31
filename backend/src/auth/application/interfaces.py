from abc import ABC, abstractmethod
from typing import Any


class ITokenProvider(ABC):
    """Token provider interface."""

    @abstractmethod
    def create_access_token(self, user_id: int, roles: list[str]) -> str:
        """Creates a new access token."""
        raise NotImplementedError

    @abstractmethod
    def create_refresh_token(self, user_id: int) -> str:
        """Creates a new refresh token."""
        raise NotImplementedError

    @abstractmethod
    def decode_token(self, token: str) -> dict[str, Any]:
        """Decodes the token."""
        raise NotImplementedError
