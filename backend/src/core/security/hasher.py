from passlib.context import CryptContext

from src.core.security.interfaces import IPasswordHasher


class PasswordHasher(IPasswordHasher):
    """Password hasher implementation."""

    def __init__(self) -> None:
        """Initializes the hasher with a secret."""
        self.pwd_context = CryptContext(
            schemes=["argon2", "bcrypt"], default="argon2", deprecated="auto"
        )

    def hash(self, password: str) -> str:
        """Hash a password.

        Args:
            password (str): The password to hash.

        Returns:
            str: The hashed password.
        """
        return self.pwd_context.hash(password)

    def verify(self, plain_password: str, hashed_password: str) -> bool:
        """Verify that a plain-text password matches a hashed password.

        Args:
            plain_password (str): The plain-text password provided by the user.
            hashed_password (str): The hashed password stored in the database.

        Returns:
            bool: True if the passwords match, False otherwise.
        """  # noqa: W505
        try:
            return self.pwd_context.verify(plain_password, hashed_password)
        except ValueError:
            return False
