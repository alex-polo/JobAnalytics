from datetime import datetime

from pydantic import BaseModel, ConfigDict

from src.modules.sources.schemas import SourceResponse


class KeywordResponse(BaseModel):
    """Schema for keyword response."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    keyword: str


class ResumeResponse(BaseModel):
    """Schema for resume response."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    is_active: bool
    created_at: datetime
    updated_at: datetime
    keywords: list[KeywordResponse]
    sources: list[SourceResponse]
