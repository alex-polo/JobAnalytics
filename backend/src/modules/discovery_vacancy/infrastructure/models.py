import enum

from sqlalchemy import Enum as SqlEnum
from sqlalchemy import ForeignKey, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.database.base import Base
from src.core.database.mixins import IntIdMixin, TimestampMixin
from src.core.database.types import (
    DataTime,
    DataTimeNullable,
    OptText,
    StatusEventTypeFieldIdx,
    Str2048,
    TextNotNull,
)
from src.modules.sources.infrastructure.models import SourceORM


class StatusRawVacancyType(enum.Enum):
    """Raw vacancy statuses."""

    NOT_DOWNLOADED = "NOT_DOWNLOADED"
    DOWNLOADED = "DOWNLOADED"
    ERROR = "ERROR"


class DiscoverySessionORM(Base, TimestampMixin, IntIdMixin):
    """Scraping session model."""

    source_id: Mapped[int] = mapped_column(
        ForeignKey("sources.id"),
        nullable=False,
    )
    session_args: Mapped[OptText]
    vacancies_found: Mapped[int] = mapped_column(default=0)
    vacancies_processed: Mapped[int] = mapped_column(default=0)
    started_at: Mapped[DataTime]
    finished_at: Mapped[DataTimeNullable]

    status: Mapped[StatusEventTypeFieldIdx]

    source: Mapped["SourceORM"] = relationship()
    errors: Mapped[list["DiscoveryErrorORM"]] = relationship(back_populates="session")


class DiscoveryErrorORM(Base, TimestampMixin, IntIdMixin):
    """Scraping error model."""

    # Исправлено: прямая ссылка на DiscoverySessionORM.id
    session_id: Mapped[int] = mapped_column(
        ForeignKey(DiscoverySessionORM.id, ondelete="CASCADE"),
        nullable=False,
    )
    error_message: Mapped[TextNotNull] = mapped_column(Text, nullable=False)
    traceback: Mapped[OptText] = mapped_column(Text, nullable=False)

    session: Mapped[DiscoverySessionORM] = relationship(back_populates="errors")


class RawVacancyORM(Base, TimestampMixin, IntIdMixin):
    """Downloaded url model."""

    session_id: Mapped[int] = mapped_column(
        ForeignKey(
            DiscoverySessionORM.id,
            ondelete="CASCADE",
        ),
        nullable=False,
    )
    source_id: Mapped[int] = mapped_column(
        ForeignKey("sources.id"),
        nullable=False,
    )
    status: Mapped[StatusRawVacancyType] = mapped_column(
        SqlEnum(StatusRawVacancyType, name="status_raw_vacancy_enum"),
        nullable=False,
        index=True,
    )

    job_title: Mapped[Str2048]
    url: Mapped[Str2048] = mapped_column(
        index=True,
    )

    body: Mapped[OptText]
    description: Mapped[OptText]
    html_content: Mapped[OptText]

    error_message: Mapped[OptText]
    error_type: Mapped[OptText]
    error_traceback: Mapped[OptText]
    errored_at: Mapped[DataTimeNullable]

    __table_args__ = (
        UniqueConstraint(
            "job_title",
            "url",
            name="uq_title_url_source",
        ),
    )
