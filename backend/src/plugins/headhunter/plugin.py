from typing import TYPE_CHECKING

from src.plugins.base import ISourcePlugin, RawVacancy, RawVacancyFromFilter

from .client import HeadHunterClient

if TYPE_CHECKING:
    from src.core.config.classes import HeadHunterClientSettings
    from src.plugins.headhunter.schemas import (
        VacancyParsingEntity,
        VacancySearchParsingEntity,
    )


class HeadHunterPlugin(ISourcePlugin):
    """Headhunter plugin."""

    def __init__(self, settings: HeadHunterClientSettings) -> None:
        """Init plugin."""
        self._setting = settings
        self._client = HeadHunterClient(settings=settings)

    def _from_filter(self, keywords: list[str]) -> list[VacancySearchParsingEntity]:
        """Convert entity to raw vacancy."""
        search_entitys: list[VacancySearchParsingEntity] = (
            self._client.get_vacancies_from_search_page(
                keywords=keywords,
                page=self._setting.filter_start_page,
                per_page=self._setting.filter_end_page,
            )
        )
        return search_entitys

    def _convert_to_raw_vacancy_filter(
        self, entitys: list[VacancySearchParsingEntity]
    ) -> list[RawVacancyFromFilter]:
        """Convert entity to raw vacancy."""
        filtered_search_entitys = [
            RawVacancyFromFilter(title=filter_vacancy.title, url=filter_vacancy.url)
            for filter_vacancy in entitys
        ]
        return filtered_search_entitys

    def discover_many(self, keywords: list[str]) -> list[RawVacancyFromFilter]:
        """Discover sources by source type."""
        filtered_search_entitys: list[VacancySearchParsingEntity] = self._from_filter(
            keywords=keywords
        )
        return self._convert_to_raw_vacancy_filter(entitys=filtered_search_entitys)

    def discover(self, keyword: str) -> list[RawVacancyFromFilter]:
        """Discover sources by source type."""
        filtered_search_entitys = self._from_filter(
            keywords=[
                keyword,
            ]
        )

        return self._convert_to_raw_vacancy_filter(entitys=filtered_search_entitys)

    def get_vacancy(self, url: str) -> RawVacancy:
        """Get vacancy by url."""
        search_entity: VacancyParsingEntity = self._client.get_vacancy(url=url)

        return RawVacancy(
            title=search_entity.title,
            url=search_entity.url,
            description=search_entity.description,
            body=search_entity.body,
            html_content=search_entity.html_content,
        )
