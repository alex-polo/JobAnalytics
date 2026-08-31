from typing import Annotated

from sqlalchemy import Column, ForeignKey, String, Table, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.database import Base
from src.core.database.mixins import IntIdMixin, TimestampMixin
from src.core.database.types import (
    DefaultFalse,
    OptStr20,
    OptStr50,
    OptStr255,
    OptStr2048,
    OptText,
    Str255,
    UniqueEmailStr,
    UniqueStr50,
)

UserIDForeignKey = Annotated[
    int,
    mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True),
]
RoleIDForeignKey = Annotated[
    int,
    mapped_column(ForeignKey("auth_roles.id", ondelete="CASCADE"), index=True),
]
HashedPassword = Annotated[
    str,
    mapped_column(String(length=128)),
]


class UserORM(Base, TimestampMixin, IntIdMixin):
    """User model."""

    email: Mapped[UniqueEmailStr]
    hashed_password: Mapped[HashedPassword]
    is_active: Mapped[DefaultFalse]
    is_verified: Mapped[DefaultFalse]

    profile: Mapped[UserProfileORM] = relationship(
        "UserProfileORM",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
        lazy="select",
    )

    roles_assignments: Mapped[list[UserRoleAssignmentORM]] = relationship(
        "UserRoleAssignmentORM",
        back_populates="user",
        uselist=True,
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        """Represent instance as a unique string."""
        return (
            f"<User(email='{self.email}', "
            f"email={self.email}, "
            f"is_active={self.is_active}, "
            f"is_verified={self.is_verified})>"
        )


class UserProfileORM(Base, TimestampMixin):
    """User profile model."""

    user_id: Mapped[UserIDForeignKey]
    first: Mapped[OptStr255]
    middle: Mapped[OptStr255]
    last: Mapped[OptStr255]
    bio: Mapped[OptText]
    avatar_url: Mapped[OptStr2048]
    timezone: Mapped[OptStr50]
    locale: Mapped[OptStr50]

    user: Mapped[UserORM] = relationship(
        "UserORM", back_populates="profile", uselist=False
    )

    __table_args__ = (UniqueConstraint("user_id", name="uq_userprofile_user_id"),)

    def __repr__(self) -> str:
        """Represent instance as a unique string."""
        return (
            f"<UserProfile(id={self.id}, "
            f"user_id={self.user_id}, "
            f"first='{self.first}', "
            f"last='{self.last}', "
            f"middle='{self.middle}', "
            f"timezone='{self.timezone}', "
            f"locale='{self.locale}')>"
        )


class AuthRoleORM(Base, TimestampMixin):
    """Auth role model."""

    name: Mapped[UniqueStr50]
    title: Mapped[Str255]
    description: Mapped[OptText]
    is_active: Mapped[DefaultFalse]

    users_assignments: Mapped[list[UserRoleAssignmentORM]] = relationship(
        "UserRoleAssignmentORM",
        back_populates="role",
        uselist=True,
        cascade="all, delete-orphan",
    )

    permissions: Mapped[list[AuthPermissionORM]] = relationship(
        secondary="association_role_permissions",
        back_populates="roles",
        uselist=True,
    )

    def __repr__(self) -> str:
        """Represent instance as a unique string."""
        return (
            f"<AuthRole(name='{self.name}', "
            f"name='{self.name}', "
            f"title='{self.title}', "
            f"description='{self.description}', "
            f"is_active={self.is_active})>"
        )


class UserRoleAssignmentORM(Base, TimestampMixin):
    """User role relation model."""

    user_id: Mapped[UserIDForeignKey]
    role_id: Mapped[RoleIDForeignKey]
    source: Mapped[OptStr20]
    reason: Mapped[OptStr255]

    __table_args__ = (UniqueConstraint("user_id", "role_id", name="uq_user_role"),)

    user: Mapped[UserORM] = relationship(
        "UserORM",
        back_populates="roles_assignments",
        uselist=False,
        lazy="select",
    )
    role: Mapped[AuthRoleORM] = relationship(
        "AuthRoleORM",
        back_populates="users_assignments",
        uselist=False,
        lazy="select",
    )

    def __repr__(self) -> str:
        """Represent instance as a unique string."""
        return f"<UserRoleAssignment(user_id={self.user_id}, role_id={self.role_id})>"


class AuthPermissionORM(Base, TimestampMixin):
    """Auth permission model."""

    name: Mapped[UniqueStr50]
    title: Mapped[Str255]
    description: Mapped[OptText]
    is_active: Mapped[DefaultFalse]

    roles: Mapped[list[AuthRoleORM]] = relationship(
        secondary="association_role_permissions",
        back_populates="permissions",
    )

    def __repr__(self) -> str:
        """Represent instance as a unique string."""
        return (
            f"<AuthPermission(name='{self.name}', "
            f"name='{self.name}', "
            f"title='{self.title}', "
            f"description='{self.description}', "
            f"is_active={self.is_active})>"
        )


association_role_permissions = Table(
    "association_role_permissions",
    Base.metadata,
    Column(
        "role_id",
        ForeignKey("auth_roles.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "permission_id",
        ForeignKey("auth_permissions.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)
