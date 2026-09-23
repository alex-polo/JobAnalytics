from sqlalchemy.orm import Mapped, relationship

from src.core.database import Base
from src.core.database.mixins import IntIdMixin, TimestampMixin
from src.core.database.types import DefaultTrue, Str100, UniqueStr20
from src.modules.resumes.infrastructure.models import resume_source_association


class SourceORM(Base, TimestampMixin, IntIdMixin):
    """Sources ORM model."""

    name: Mapped[Str100]
    code: Mapped[UniqueStr20]
    base_url: Mapped[str]
    is_active: Mapped[DefaultTrue]

    resumes: Mapped[list["ResumeORM"]] = relationship(  # type: ignore
        secondary=resume_source_association,
        back_populates="sources",
    )
