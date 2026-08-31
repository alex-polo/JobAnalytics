from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr


class BaseDomain(BaseModel):
    """Base domain entity."""

    model_config = ConfigDict(from_attributes=True)


class RoleEntity(BaseDomain):
    """Role domain entity."""

    model_config = ConfigDict(from_attributes=True)

    id: int | None = None
    name: str
    title: str
    description: str | None = None
    is_active: bool = False


class ProfileEntity(BaseDomain):
    """Profile domain entity."""

    first: str | None = None
    last: str | None = None
    middle: str | None = None
    bio: str | None = None
    avatar_url: str | None = None
    timezone: str | None = None
    locale: str | None = None


class UserRoleAssignmentEntity(BaseDomain):
    """User role assignment domain entity."""

    id: int | None = None
    user_id: int
    role_id: int
    source: str | None = None
    reason: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    role: RoleEntity | None = None


class UserEntity(BaseDomain):
    """User domain entity."""

    id: int | None = None
    email: EmailStr
    hashed_password: str
    is_active: bool = False
    is_verified: bool = False
    created_at: datetime | None = None
    updated_at: datetime | None = None

    profile: ProfileEntity | None = None
    roles_assignments: list[UserRoleAssignmentEntity] | None = None

    @property
    def user_roles(self) -> list[str]:
        """Return user's email."""
        if not self.roles_assignments:
            return []

        user_roles = [
            a.role.name for a in self.roles_assignments if a.role and a.role.is_active
        ]

        return user_roles
