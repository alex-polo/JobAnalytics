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


class ISourcePlugin:
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


class IAIPlugin(ABC):
    """Base class for AI plugins."""

    @abstractmethod
    async def analyze_vacancy(self, vacancy_data: dict): ...  # noqa: ANN201, D102

    @abstractmethod
    async def match_resume(self, vacancy: dict, resume: dict): ...  # noqa: ANN201, D102
