from pydantic import BaseModel


class BearerToken(BaseModel):
    """Bearer token schema."""

    access_token: str
    token_type: str = "bearer"  # noqa: S105
