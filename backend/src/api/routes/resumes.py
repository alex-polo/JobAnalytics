from typing import TYPE_CHECKING

from fastapi import APIRouter

from src.api.dependencies import ResumesServiceDep  # noqa: TC001
from src.modules.resumes.schemas import ResumeResponse

if TYPE_CHECKING:
    from src.modules.resumes.infrastructure.models import ResumeORM

resumes_router = APIRouter(prefix="/resumes", tags=["resumes"])


@resumes_router.get("/", response_model=list[ResumeResponse])
async def get_resumes(service: ResumesServiceDep) -> list[ResumeResponse]:
    """Get all active resumes."""
    resumes: list[ResumeORM] = await service.get_all()
    return resumes  # type: ignore
