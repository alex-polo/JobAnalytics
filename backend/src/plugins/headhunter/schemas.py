from pydantic import BaseModel


class VacancySearchParsingEntity(BaseModel):
    """Vacancy search entity."""

    title: str
    url: str


class VacancyParsingEntity(BaseModel):
    """Vacancy entity."""

    title: str
    url: str
    description: str
    body: str
