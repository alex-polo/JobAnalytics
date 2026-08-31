import json
from typing import TYPE_CHECKING, Any
from unittest.mock import MagicMock

from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from starlette.responses import JSONResponse

from src.core.exceptions.base import EntityNotFoundError
from src.core.exceptions.handlers import (
    app_error_handler,
    sqlalchemy_exception_handler,
    universal_exception_handler,
    validation_exception_handler,
)

if TYPE_CHECKING:
    from fastapi.responses import JSONResponse


def test_app_error_handler_coverage() -> None:
    """Test app_error_handler directly."""
    request = MagicMock()
    request.url.path = "/api/v1/test-path"

    custom_exc = EntityNotFoundError(entity="TestEntity", entity_id=23)

    response: JSONResponse = app_error_handler(request, custom_exc)

    assert response.status_code == 404

    data: dict[str, Any] = json.loads(bytes(response.body).decode())

    assert "error" in data
    error_obj: dict[str, Any] = data["error"]

    assert error_obj["code"] == "ERR_ENTITY_NOT_FOUND"
    assert error_obj["details"]["entity"] == "TestEntity"
    assert error_obj["details"]["entity_id"] == 23
    assert "TestEntity" in error_obj["message"]


def test_universal_handler_coverage() -> None:
    """Test universal_exception_handler directly."""
    request = MagicMock()
    request.url.path = "/critical-error"
    exc = RuntimeError("Unknown error")

    response: JSONResponse = universal_exception_handler(request, exc)

    assert response.status_code == 500
    data: dict[str, Any] = json.loads(bytes(response.body).decode())
    assert "error" in data
    error_obj: dict[str, Any] = data["error"]
    assert error_obj["code"] == "INTERNAL_SERVER_ERROR"


def test_validation_handler_coverage() -> None:
    """Test validation_exception_handler directly."""
    request = MagicMock()
    request.url.path = "/api/v1/items"

    errors = [
        {
            "loc": ("body", "item_id"),
            "msg": "field required",
            "type": "value_error.missing",
        }
    ]
    exc = RequestValidationError(errors)

    response: JSONResponse = validation_exception_handler(request, exc)

    assert response.status_code == 422
    data: dict[str, Any] = json.loads(bytes(response.body).decode())

    assert "error" in data
    error_obj: dict[str, Any] = data["error"]

    assert error_obj["code"] == "VALIDATION_ERROR"
    assert "body.item_id" in error_obj["details"]


def test_sqlalchemy_handler_coverage() -> None:
    """Test sqlalchemy_exception_handler directly."""
    request = MagicMock()
    request.url.path = "/db-op"

    exc_base = SQLAlchemyError("Connection lost")
    resp_base: JSONResponse = sqlalchemy_exception_handler(request, exc_base)
    assert resp_base.status_code == 500

    exc_integrity = IntegrityError("insert...", {}, Exception("Duplicate"))
    resp_integrity: JSONResponse = sqlalchemy_exception_handler(request, exc_integrity)

    assert resp_integrity.status_code == 400
    data: dict[str, Any] = json.loads(bytes(resp_integrity.body).decode())
    assert "error" in data
    error_obj: dict[str, Any] = data["error"]

    assert error_obj["code"] == "INTEGRITY_ERROR"
