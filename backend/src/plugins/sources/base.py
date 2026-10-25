from abc import ABC, abstractmethod
from typing import NamedTuple


class RawVacancyFromFilter(NamedTuple):
    """Base class for raw vacancies from filter."""

    title: str
    url: str


class RawVacancy(NamedTuple):
    """Base class for raw vacancies."""

    title: str
    url: str
    description: str
    body: str
    html_content: str


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
