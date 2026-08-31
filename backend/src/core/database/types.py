from datetime import datetime
from typing import Annotated

from sqlalchemy import TIMESTAMP, Boolean, String, Text, false, func
from sqlalchemy.orm import mapped_column

from src.core.utils import utcnow

IntPk = Annotated[int, mapped_column(primary_key=True)]
DefaultFalse = Annotated[
    bool, mapped_column(Boolean, default=False, server_default=false())
]
UniqueEmailStr = Annotated[
    str, mapped_column(String(length=255), unique=True, index=True)
]
UniqueStr50 = Annotated[str, mapped_column(String(length=50), unique=True)]
Str255 = Annotated[str, mapped_column(String(length=255))]
OptStr20 = Annotated[str | None, mapped_column(String(length=20))]
OptStr50 = Annotated[str | None, mapped_column(String(length=50))]
OptStr255 = Annotated[str | None, mapped_column(String(length=255))]
OptStr2048 = Annotated[str | None, mapped_column(String(length=2048))]
OptText = Annotated[str | None, mapped_column(Text)]

CreatedAt = Annotated[
    datetime,
    mapped_column(TIMESTAMP(timezone=True), default=utcnow, server_default=func.now()),
]

UpdatedAt = Annotated[
    datetime,
    mapped_column(
        TIMESTAMP(timezone=True),
        default=utcnow,
        onupdate=utcnow,
        server_default=func.now(),
        server_onupdate=func.now(),
    ),
]

__all__ = (
    "CreatedAt",
    "DefaultFalse",
    "IntPk",
    "OptStr20",
    "OptStr50",
    "OptStr255",
    "OptStr2048",
    "OptText",
    "Str255",
    "UniqueEmailStr",
    "UniqueStr50",
    "UpdatedAt",
)
