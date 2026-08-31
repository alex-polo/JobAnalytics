from pydantic import BaseModel


class CookieSettings(BaseModel):
    """Cookie settings."""

    name: str
    max_age: int
    path: str
    domain: str | None
    secure: bool
    samesite: str


class TokenEntity(BaseModel):
    """Token entity."""

    access_token: str
    refresh_token: str
    token_type: str = "bearer"  # noqa: S105
    cookie_settings: CookieSettings
