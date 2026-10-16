from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.core.database.base import Base
from src.core.database.mixins import IntIdMixin, TimestampMixin
from src.core.database.types import (
    StatusEventTypeFieldIdx,
    Str100,
)


class QueueAnalyzeVacancyORM(Base, TimestampMixin, IntIdMixin):
    """Queue matching model."""

    status: Mapped[StatusEventTypeFieldIdx]

    vacancy_id: Mapped[int] = mapped_column(
        ForeignKey("raw_vacancys.id", ondelete="CASCADE"),
        index=True,
    )
    keyword: Mapped[Str100]
