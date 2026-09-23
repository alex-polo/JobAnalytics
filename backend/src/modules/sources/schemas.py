from pydantic import BaseModel, ConfigDict


class SourceResponse(BaseModel):
    """Schema for source response."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    code: str
