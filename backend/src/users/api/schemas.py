from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr


class ApiBaseModel(BaseModel):
    """Base model for API schemas."""

    model_config = ConfigDict(from_attributes=True)


class ProfileCreateSchema(ApiBaseModel):
    """Profile create schema class."""

    first: str | None = None
    last: str | None = None
    middle: str | None = None
    bio: str | None = None
    avatar_url: str | None = None
    timezone: str | None = None
    locale: str | None = None


class UserCreateSchema(ApiBaseModel):
    """User create schema class."""

    email: EmailStr
    password: str
    is_active: bool = False
    is_verified: bool = False

    profile: ProfileCreateSchema | None = None


class RoleCreateSchema(ApiBaseModel):
    """User create schema class."""

    name: str
    title: str
    description: str | None = None
    is_active: bool


class ProfileReadSchema(ApiBaseModel):
    """Profile read schema class."""

    id: int
    first: str | None = None
    last: str | None = None
    middle: str | None = None
    bio: str | None = None
    avatar_url: str | None = None
    timezone: str | None = None
    locale: str | None = None


class RoleReadSchema(ApiBaseModel):
    """Role read schema class."""

    id: int
    name: str
    title: str
    description: str | None = None
    is_active: bool


class UserRoleAssignmentReadSchema(ApiBaseModel):
    """User role assignment read schema class."""

    id: int
    user_id: int
    role_id: int
    source: str | None = None
    reason: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    role: RoleReadSchema


class UserReadSchema(ApiBaseModel):
    """User read schema class."""

    id: int
    email: EmailStr
    is_active: bool
    is_verified: bool
    profile: ProfileReadSchema | None = None
    roles_assignments: list[UserRoleAssignmentReadSchema] | None = None
