from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from src.core.database.base import Base
from src.core.database.mixins import IntIdMixin, TimestampMixin
from src.core.database.types import (
    DataTimeNullable,
    IntNotNullDefault0,
    OptText,
    StatusEventTypeFieldIdx,
    Str100,
)


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
    score: Mapped[float]

    __table_args__ = (UniqueConstraint("resume_id", "vacancy_id"),)
