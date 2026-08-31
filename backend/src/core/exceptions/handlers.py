"""Exception handlers for the FastAPI application.

This module provides unified error handling across all app layers,
ensuring a consistent JSON response format.

Supported HTTP Status Codes:
    - 400: IntegrityError, DuplicateError (Bad Request).
    - 401: Unauthorized access (from Starlette or Auth logic).
    - 403: Forbidden actions or CSRF/CORS issues.
    - 404: Resource not found (EntityNotFoundError or wrong Path).
    - 405: Method not allowed (e.g., POST on GET endpoint).
    - 409: Conflict (ForeignKeyViolationError, DuplicateError).
    - 422: Pydantic validation failures (RequestValidationError).
    - 500: Unexpected server errors (Internal Server Error).

Example App Usage:
    ```python
    from fastapi import FastAPI
    from src.core.exceptions.handlers import register_exceptions
    from src.core.schemas.error import ErrorSchema

    app = FastAPI(
        responses={
            400: {"model": ErrorSchema},
            404: {"model": ErrorSchema},
            500: {"model": ErrorSchema},
        }
    )
    register_exceptions(app)
    ```
"""

import logging
from collections.abc import Callable, Coroutine
from typing import TYPE_CHECKING, Any, cast

from fastapi import FastAPI, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from starlette.exceptions import HTTPException as StarletteHTTPException

from src.core.schemas.error import ErrorDetail, ErrorSchema

from .base import AppBaseError

if TYPE_CHECKING:
    from fastapi import Request


log = logging.getLogger(__name__)

type HandlerType = Callable[[Request, Any], Coroutine[Any, Any, JSONResponse]]


def app_error_handler(request: Request, exc: AppBaseError) -> JSONResponse:
    """Handles custom application-level exceptions.

    Converts internal AppBaseError instances into a standardized
    JSONResponse using the exception's metadata.

    Args:
        request: The incoming Starlette/FastAPI request object.
        exc: The raised AppBaseError instance containing error details.

    Returns:
        A JSONResponse with the appropriate status code and ErrorSchema.
    """
    log.error("Application server error: %s", exc, exc_info=exc)

    error_data = ErrorSchema(
        error=ErrorDetail(
            type=exc.__class__.__name__,
            code=exc.error_code,
            message=exc.message,
            path=request.url.path,
            details=exc.to_details(),
        )
    )

    return JSONResponse(
        status_code=exc.status_code,
        content=error_data.model_dump(),
    )


def universal_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handles uncaught exceptions as a last-resort safety net.

    Catches any exception not handled by more specific handlers,
    returning a generic 500 response to avoid exposing stack traces
    or sensitive internal details to the client.

    Args:
        request: The incoming Starlette/FastAPI request object.
        exc: The unhandled exception that was raised.

    Returns:
        A JSONResponse with HTTP 500 and a user-friendly message.
    """
    log.error("Unhandled error occurred in request: %s", exc)

    error_data = ErrorSchema(
        error=ErrorDetail(
            type=exc.__class__.__name__,
            code="INTERNAL_SERVER_ERROR",
            message="Something went wrong on our side",
            path=request.url.path,
            details=None,
        )
    )
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=error_data.model_dump(),
    )


def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    """Handles Pydantic request validation failures.

    Processes RequestValidationError from FastAPI when request bodies,
    query parameters, or path parameters fail Pydantic validation.
    Returns a structured response with field-level error details.

    Args:
        request: The incoming Starlette/FastAPI request object.
        exc: The RequestValidationError containing validation failures.

    Returns:
        A JSONResponse with HTTP 422 and detailed field errors.
    """
    log.error("Validation error occurred in request: %s", exc, exc_info=exc)

    validation_details = {
        ".".join(str(loc) for loc in err["loc"]): err["msg"] for err in exc.errors()
    }

    error_data = ErrorSchema(
        error=ErrorDetail(
            type=exc.__class__.__name__,
            code="VALIDATION_ERROR",
            message="Invalid input data",
            path=request.url.path,
            details=validation_details,
        )
    )
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        content=error_data.model_dump(),
    )


def sqlalchemy_exception_handler(
    request: Request,
    exc: SQLAlchemyError,
) -> JSONResponse:
    """Handles exceptions while hiding technical implementation details.

    Maps low-level SQLAlchemy errors (like IntegrityError) to user-friendly
    400/500 responses without exposing SQL queries or table structures.

    Args:
        request: The incoming Starlette/FastAPI request object.
        exc: The SQLAlchemy exception encountered during DB operations.

    Returns:
        A secure JSONResponse that prevents sensitive data leakage.
    """  # noqa: W505
    log.error("Database error occurred at %s: %s", request.url.path, exc, exc_info=exc)

    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    error_code = "DATABASE_ERROR"
    message = "An unexpected database error occurred."

    if isinstance(exc, IntegrityError):
        status_code = status.HTTP_400_BAD_REQUEST
        error_code = "INTEGRITY_ERROR"
        message = "Data integrity violation (duplicate entry or constraint violation)."

    error_data = ErrorSchema(
        error=ErrorDetail(
            type=exc.__class__.__name__,
            code=error_code,
            message=message,
            path=request.url.path,
            details=None,
        ),
    )
    return JSONResponse(status_code=status_code, content=error_data.model_dump())


def http_exception_handler(
    request: Request, exc: StarletteHTTPException
) -> JSONResponse:
    """Handles standard HTTP exceptions from Starlette/FastAPI.

    Catches built-in HTTP exceptions (401, 403, 404, 405, etc.) raised
    by FastAPI routing, authentication, or authorization logic.
    Converts them to a consistent ErrorSchema response format.

    Args:
        request: The incoming Starlette/FastAPI request object.
        exc: The Starlette HTTPException with status code and detail.

    Returns:
        A JSONResponse with the original status code and error details.
    """
    log.error("HTTP error %s at %s: %s", exc.status_code, request.url.path, exc.detail)

    error_code = f"HTTP_{exc.status_code}_ERROR"

    error_data = ErrorSchema(
        error=ErrorDetail(
            type=exc.__class__.__name__,
            code=error_code,
            message=exc.detail,
            path=request.url.path,
            details=None,
        )
    )
    return JSONResponse(status_code=exc.status_code, content=error_data.model_dump())


def register_exceptions(app: FastAPI) -> None:
    """Registers global exception handlers for the FastAPI application.

    Handlers are registered to ensure that the most specific exceptions
    are caught first. The resolution order is:
    1. RequestValidationError: Pydantic schema validation failures.
    2. StarletteHTTPException: Framework-level errors (404, 401, 405).
    3. SQLAlchemyError: Database integrity and connectivity issues.
    4. AppBaseError: Custom domain and business logic exceptions.
    5. Exception: A final fallback for any unhandled 500 errors.

    Args:
        app: The FastAPI application instance to configure.
    """
    app.add_exception_handler(
        RequestValidationError,
        cast("HandlerType", validation_exception_handler),
    )
    app.add_exception_handler(
        StarletteHTTPException,
        cast("HandlerType", http_exception_handler),
    )

    app.add_exception_handler(
        SQLAlchemyError,
        cast("HandlerType", sqlalchemy_exception_handler),
    )

    app.add_exception_handler(
        AppBaseError,
        cast("HandlerType", app_error_handler),
    )

    app.add_exception_handler(
        Exception,
        cast("HandlerType", universal_exception_handler),
    )


__all__ = ("register_exceptions",)
