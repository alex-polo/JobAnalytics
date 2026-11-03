from src.plugins.sources.base import RawVacancy
from src.plugins.sources.headhunter.schemas import VacancyParsingEntity


class VacancyParsingEntityV2(VacancyParsingEntity):
    """Base class for vacancy parsing entity version 2."""

    salary: str | None
    experience: str | None
    employment: str | None
    civil_contract: str | None
    schedule: str | None
    working_hours: str | None
    work_formats: str | None
    company_name: str | None


class RawVacancyV2(RawVacancy):
    """Base class for raw vacancies version 2."""

    title: str
    url: str
    description: str
    body: str
    html_content: str
