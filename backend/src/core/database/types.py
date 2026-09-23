from datetime import datetime
from typing import Annotated

from sqlalchemy import TIMESTAMP, Boolean, String, Text, false, func, true
from sqlalchemy.orm import mapped_column

from src.core.utils import utcnow

IntPk = Annotated[int, mapped_column(primary_key=True)]
DefaultFalse = Annotated[
    bool,
    mapped_column(
        Boolean(),
        default=False,
        server_default=false(),
    ),
]

DefaultTrue = Annotated[
    bool,
    mapped_column(
        Boolean(),
        default=True,
        server_default=true(),
    ),
]

# Unique types
UniqueEmailStr = Annotated[
    str, mapped_column(String(length=255), unique=True, index=True)
]
UniqueStr50 = Annotated[str, mapped_column(String(length=50), unique=True)]
UniqueStr20 = Annotated[str, mapped_column(String(length=20), unique=True)]

# Not null str types
Str20 = Annotated[str, mapped_column(String(length=20))]
Str100 = Annotated[str, mapped_column(String(length=100))]
Str255 = Annotated[str, mapped_column(String(length=255))]
TextNotNull = Annotated[str, mapped_column(Text())]

# Optional str types
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
    "Str20",
    "Str100",
    "Str255",
    "TextNotNull",
    "UniqueEmailStr",
    "UniqueStr50",
    "UpdatedAt",
)
