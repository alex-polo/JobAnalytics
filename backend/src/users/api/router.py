from fastapi import APIRouter

from src.auth.api.dependencies import CurrentUserDep  # noqa: TC001
from src.users.api.schemas import UserReadSchema
from src.users.domain.entities import UserEntity  # noqa: TC001

user_router = APIRouter(prefix="/users", tags=["users"])


@user_router.get("/me", response_model=UserReadSchema)
async def get_current_user_profile(
    current_user: CurrentUserDep,
) -> UserEntity:
    """Get current user."""
    return current_user
