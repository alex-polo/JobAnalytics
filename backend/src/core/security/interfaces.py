from abc import ABC, abstractmethod


class IPasswordHasher(ABC):
    """Password hasher interface."""

    @abstractmethod
    def hash(self, password: str) -> str:
        """Hashes a password."""
        raise NotImplementedError

    @abstractmethod
    def verify(self, password: str, hashed_password: str) -> bool:
        """Verifies a password."""
        raise NotImplementedError
