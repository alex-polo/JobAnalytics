from typing import Any

from fastapi import status


class AppBaseError(Exception):
    """Base exception for the application."""

    def __init__(
        self,
        status_code: int,
        message: str,
        error_code: str | None = None,
    ) -> None:
        """Initialize exception."""
        self.status_code = status_code
        self.message = message
        self.error_code = error_code or f"ERR_{status_code}"

    def to_details(self) -> dict[str, Any] | None:
        """Convert exception to details."""
        excluded: set[str] = {"status_code", "message", "error_code"}
        details: dict[str, Any] = {
            k: v
            for k, v in self.__dict__.items()
            if k not in excluded and v is not None
        }
        return details if details else None


# ─────────────────────────────────────────
# Repository Layer
# ─────────────────────────────────────────
class RepositoryError(AppBaseError):
    """Base repository error."""

    def __init__(
        self,
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        message: str = "Repository error",
        error_code: str = "ERR_REPO",
    ) -> None:
        """Initialize exception."""
        super().__init__(
            status_code=status_code,
            message=message,
            error_code=error_code,
        )


class DomainError(AppBaseError):
    """Base domain error."""


class ApplicationError(AppBaseError):
    """Base application error."""


class InfrastructureError(AppBaseError):
    """Base infrastructure error."""


class EntityNotFoundError(RepositoryError):
    """Entity not found in DB."""

    def __init__(
        self,
        message: str = "Entity not found",
        entity: str | None = None,
        entity_id: int | str | None = None,
    ) -> None:
        """Initialize exception."""
        msg_parts = []
        if entity:
            msg_parts.append(f"entity: {entity}")
        if entity_id:
            msg_parts.append(f"id: {entity_id}")

        full_message = f"{message} ({', '.join(msg_parts)})" if msg_parts else message

        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            message=full_message,
            error_code="ERR_ENTITY_NOT_FOUND",
        )

        self.entity = entity
        self.entity_id = entity_id


class DuplicateError(RepositoryError):
    """Duplicate entity (unique constraint violation)."""

    def __init__(
        self,
        field: str,
        value: str | int | None = None,
        message: str | None = None,
    ) -> None:
        """Initialize exception."""
        if message is None:
            if value is not None:
                message = f"Entity with {field}='{value}' already exists"
            else:
                message = f"Entity with {field} already exists"

        super().__init__(
            message=message,
            status_code=status.HTTP_409_CONFLICT,
            error_code="ERR_DUPLICATE",
        )
        self.field = field
        self.value = value


class ForeignKeyViolationError(RepositoryError):
    """Foreign key constraint violation."""

    def __init__(
        self,
        referenced_entity: str | None = None,
        constraint: str | None = None,
        message: str | None = None,
    ) -> None:
        """Initialize exception."""
        if message is None:
            if referenced_entity:
                message = f"Cannot delete: referenced by {referenced_entity}"
            elif constraint:
                message = f"Foreign key constraint '{constraint}' violated"
            else:
                message = "Foreign key constraint violated"

        super().__init__(
            message=message,
            status_code=status.HTTP_409_CONFLICT,
            error_code="ERR_FK_VIOLATION",
        )
        self.referenced_entity = referenced_entity
        self.constraint = constraint


# ─────────────────────────────────────────
# Service Layer
# ─────────────────────────────────────────
class ServiceError(AppBaseError):
    """Base service error."""

    def __init__(
        self,
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        message: str = "Service error",
        error_code: str = "ERR_SERVICE",
    ) -> None:
        """Initialize exception."""
        super().__init__(status_code, message, error_code)
