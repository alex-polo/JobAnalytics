from typing import Annotated

from fastapi import Depends

from .hasher import PasswordHasher
from .interfaces import IPasswordHasher


def get_password_hasher() -> IPasswordHasher:
    """Returns a PasswordHasher instance."""
    return PasswordHasher()


PasswordHasherDep = Annotated[IPasswordHasher, Depends(get_password_hasher)]
