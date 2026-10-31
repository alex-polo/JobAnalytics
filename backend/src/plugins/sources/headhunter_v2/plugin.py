from typing import TYPE_CHECKING

from src.plugins.sources.base import RawVacancy
from src.plugins.sources.headhunter.plugin import HeadHunterPlugin

from .parsers import parsing_vacancy_page

if TYPE_CHECKING:
    from src.core.config.classes import HeadHunterClientSettings
    from src.plugins.sources.headhunter_v2.schemas import VacancyParsingEntityV2


class HeadHunterPluginV2(HeadHunterPlugin):
    """Headhunter plugin."""

    def __init__(self, settings: HeadHunterClientSettings) -> None:
        """Init plugin."""
        super().__init__(settings=settings)

    def get_vacancy(self, url: str) -> RawVacancy:
        """Get vacancy from url."""
        html_content = self._client.load_html_content(url=url)
        parsed_data: VacancyParsingEntityV2 = parsing_vacancy_page(
            html_content=html_content,
            url=url,
        )

        return RawVacancy(
            title=parsed_data.title,
            url=parsed_data.url,
            description=parsed_data.description,
            body=parsed_data.body,
            html_content=parsed_data.html_content,
        )
