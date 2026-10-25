from typing import Annotated

from sqlalchemy import Enum, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from src.core.database.base import Base
from src.core.database.mixins import IntIdMixin, TimestampMixin
from src.core.database.types import (
    DataTimeNullable,
    DefaultFalse,
    IntNotNullDefault0,
    IntNotNullIdx,
    JsonB,
    OptBoolean,
    OptText,
    StatusEventTypeFieldIdx,
    Str100,
    Str255,
    Str2048,
    TextNotNull,
)
from src.modules.matching_vacancy.domain import MatchLevel


class QueueMatchingORM(Base, TimestampMixin, IntIdMixin):
    """Queue matching model."""

    status: Mapped[StatusEventTypeFieldIdx]

    vacancy_id: Mapped[int] = mapped_column(
        ForeignKey("raw_vacancys.id", ondelete="CASCADE"),
        index=True,
    )
    resume_id: Mapped[int] = mapped_column(
        ForeignKey("resumes.id", ondelete="CASCADE"),
        index=True,
    )
    keyword: Mapped[Str100]
    attempts: Mapped[IntNotNullDefault0]

    error_message: Mapped[OptText]
    error_type: Mapped[OptText]
    error_traceback: Mapped[OptText]
    errored_at: Mapped[DataTimeNullable]

    __table_args__ = (
        UniqueConstraint(
            "vacancy_id",
            "resume_id",
            name="uq_queue_matching_vacancy_resume",
        ),
    )


MatchLevelFieldIdx = Annotated[
    MatchLevel,
    mapped_column(
        Enum(MatchLevel, name="match_level_enum"), nullable=False, index=True
    ),
]


class ResumeMatchResultORM(Base, TimestampMixin, IntIdMixin):
    """Resume match result model."""

    resume_id: Mapped[int] = mapped_column(
        ForeignKey("resumes.id", ondelete="CASCADE"),
        index=True,
    )

    vacancy_id: Mapped[int] = mapped_column(
        ForeignKey("raw_vacancys.id", ondelete="CASCADE"),
        index=True,
    )

    url: Mapped[Str2048]
    keyword: Mapped[Str255]

    match_score: Mapped[IntNotNullIdx]
    match_level: Mapped[MatchLevelFieldIdx]

    matching_skills: Mapped[JsonB]
    missing_skills: Mapped[JsonB]
    extra_skills: Mapped[JsonB]

    experience_match: Mapped[DefaultFalse]
    level_match: Mapped[DefaultFalse]
    location_match: Mapped[DefaultFalse]
    salary_match: Mapped[OptBoolean]
    is_remote: Mapped[DefaultFalse]

    summary: Mapped[TextNotNull]
    strengths: Mapped[JsonB]
    gaps: Mapped[JsonB]
    recommendation: Mapped[TextNotNull]

    __table_args__ = (
        UniqueConstraint(
            "resume_id",
            "vacancy_id",
            name="uq_match_result_resume_vacancy",
        ),
    )
