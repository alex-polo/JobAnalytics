from fastapi import APIRouter
from fastapi.responses import JSONResponse

from src.auth.api import auth_router
from src.core.config import APP_SETTINGS
from src.users.api.router import user_router

api_v1_router = APIRouter(
    prefix=APP_SETTINGS.API_PREFIX.v1.prefix,
)

utils_router = APIRouter(prefix="/utils")


@utils_router.get("/health-check", tags=["utils"])
async def health_check() -> JSONResponse:
    """Health check."""
    return JSONResponse(
        content={"status": "healthy"},
    )


api_v1_router.include_router(utils_router)

api_v1_router.include_router(auth_router)

api_v1_router.include_router(user_router)
