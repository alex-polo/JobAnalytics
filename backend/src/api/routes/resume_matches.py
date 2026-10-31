from typing import Annotated

from fastapi import APIRouter, Query

from src.api.dependencies import (  # noqa: TC001
    ResumeMatchingServiceDep,
)
from src.core.exceptions.base import EntityNotFoundError
from src.modules.matching_vacancy.domain import (
    LocationItems,
    MatchLevel,
    ResumeMatchListItem,
)
from src.modules.matching_vacancy.domain.schemas import ResumeMatchDetails

resume_matches_router = APIRouter(prefix="/resume-matches", tags=["resume-matches"])


@resume_matches_router.get(
    "",
    response_model=list[ResumeMatchListItem],
    response_model_by_alias=True,
)
async def get_resume_matches(
    service: ResumeMatchingServiceDep,
    q: Annotated[str | None, Query(description="Поиск по вакансии/резюме")] = None,
    match_level: Annotated[MatchLevel | None, Query()] = None,
    location: Annotated[LocationItems | None, Query()] = None,
    date: str | None = None,
) -> list[ResumeMatchListItem]:
    """Get all active resumes."""
    matches_list: list[ResumeMatchListItem] = await service.get_matches_list(
        q=q,
        match_level=match_level,
        location=location,
        date=date,
    )
    return matches_list


@resume_matches_router.get(
    "/{match_id}",
    response_model=ResumeMatchDetails,
    response_model_by_alias=True,
)
async def get_resume_match_details(
    match_id: int,
    service: ResumeMatchingServiceDep,
) -> ResumeMatchDetails:
    """Get resume match details."""
    match = await service.get_match_details(match_id)

    if match is None:
        raise EntityNotFoundError(entity_id=match_id, entity="match")

    return match
