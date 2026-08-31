from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import (
    DeclarativeBase,
    declared_attr,
)

from src.core.config import APP_SETTINGS
from src.core.database.mixins import IntIdMixin
from src.core.utils import camel_to_snake


class Base(AsyncAttrs, DeclarativeBase, IntIdMixin):
    """Base class for all models."""

    __abstract__ = True

    metadata = MetaData(
        naming_convention=APP_SETTINGS.DATABASE.naming_convention,
    )

    @declared_attr.directive
    def __tablename__(cls) -> str:
        """Return the table name for the model."""
        return camel_to_snake(cls.__name__)
