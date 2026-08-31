import logging
import time
import uuid
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Awaitable, Callable

    from fastapi import FastAPI, Request, Response


log = logging.getLogger(__name__)


async def observability_middleware(
    request: Request,
    call_next: Callable[[Request], Awaitable[Response]],
) -> Response:
    """Add request ID for tracing."""
    start_time = time.perf_counter()
    request_id = request.headers.get("X-Request-ID", uuid.uuid4().hex[:12])

    try:
        response: Response = await call_next(request)

        process_time = time.perf_counter() - start_time

        response.headers["X-Request-ID"] = f"req_{request_id}"
        response.headers["X-Process-Time"] = f"{process_time:.4f}s"

        log.info(
            "[%s] %s %s -> %s (%.3fs)",
            request_id,
            request.method,
            request.url.path,
            response.status_code,
            process_time,
        )

        return response
    except Exception as e:
        process_time = time.perf_counter() - start_time
        log.error(
            "[%s] %s %s -> FAILED (%.3fs): %s",
            request_id,
            request.method,
            request.url.path,
            process_time,
            e,
        )
        raise e


def register_middlewares(app: FastAPI) -> None:
    """Register middleware."""
    app.middleware("http")(observability_middleware)


__all__ = ("register_middlewares",)
