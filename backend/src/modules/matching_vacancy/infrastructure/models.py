from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from src.core.database.base import Base
from src.core.database.mixins import IntIdMixin, TimestampMixin
from src.core.database.types import (
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

    __table_args__ = (UniqueConstraint("vacancy_id", "resume_id"),)
