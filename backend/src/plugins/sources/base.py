from abc import ABC, abstractmethod
from typing import NamedTuple


class RawVacancyFromFilter(NamedTuple):
    """Base class for raw vacancies from filter."""

    external_id: str
    title: str
    url: str


class RawVacancy(NamedTuple):
    """Base class for raw vacancies."""

    title: str
    url: str
    description: str
    body: str
    html_content: str
    salary: str | None = None
    experience: str | None = None
    employment: str | None = None
    civil_contract: str | None = None
    schedule: str | None = None
    working_hours: str | None = None
    work_formats: str | None = None
    company_name: str | None = None


class ISourcePlugin(ABC):
    """Base class for source plugins."""

    @abstractmethod
    def discover_many(self, keywords: list[str]) -> list[RawVacancyFromFilter]:
        """Discover sources by source type."""

    @abstractmethod
    def discover(self, keyword: str) -> list[RawVacancyFromFilter]:
        """Discover sources by source type."""

    @abstractmethod
    def get_vacancy(self, url: str) -> RawVacancy:
        """Get vacancy by url."""
