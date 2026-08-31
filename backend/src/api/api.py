from fastapi import APIRouter

from src.core.config import APP_SETTINGS

from .api_v1 import api_v1_router

api_router = APIRouter(prefix=APP_SETTINGS.API_PREFIX.prefix)

api_router.include_router(api_v1_router)

__all__ = ("api_router",)
