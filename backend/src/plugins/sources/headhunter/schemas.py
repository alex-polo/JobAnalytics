from pydantic import BaseModel


class VacancySearchParsingEntity(BaseModel):
    """Vacancy search entity."""

    external_id: str
    title: str
    url: str


class VacancyParsingEntity(BaseModel):
    """Vacancy entity."""

    title: str
    url: str
    description: str
    body: str
    html_content: str
