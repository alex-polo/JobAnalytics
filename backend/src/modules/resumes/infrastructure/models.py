from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.database import Base
from src.core.database.mixins import IntIdMixin, TimestampMixin
from src.core.database.types import DefaultTrue, Str100, Str255, TextNotNull


class ResumeORM(Base, TimestampMixin, IntIdMixin):
    """Resumes ORM model."""

    name: Mapped[Str255]
    text: Mapped[TextNotNull]
    is_active: Mapped[DefaultTrue]

    keywords: Mapped[list[KeywordsResumeORM]] = relationship(
        back_populates="resume",
        cascade="all, delete-orphan",
    )

    sources: Mapped[list["SourceORM"]] = relationship(  # type: ignore
        secondary="resume_source_association",
        back_populates="resumes",
    )


class KeywordsResumeORM(Base, TimestampMixin, IntIdMixin):
    """KeywordsResumes ORM model."""

    keyword: Mapped[Str100]
    resume_id: Mapped[int] = mapped_column(ForeignKey("resumes.id"), nullable=False)

    resume: Mapped[ResumeORM] = relationship(back_populates="keywords")


resume_source_association = Table(
    "resume_source_association",
    Base.metadata,
    Column("resume_id", ForeignKey("resumes.id"), primary_key=True),
    Column("source_id", ForeignKey("sources.id"), primary_key=True),
)
