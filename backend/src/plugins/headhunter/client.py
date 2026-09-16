import logging
from time import sleep
from typing import TYPE_CHECKING, Any

import httpx

from .constants import DEFAULT_CLIENT_HEADERS
from .exceptions import (
    HeadHunterDownloadPageError,
    HeadHunterSearchPageParsingError,
    HeadHunterVacancyPageParsingError,
)
from .parsers import parse_vacancy_page, parsing_search_page

if TYPE_CHECKING:
    from src.core.config import HeadHunterClientSettings

    from .schemas import VacancyParsingEntity, VacancySearchParsingEntity


log = logging.getLogger(__name__)


class HeadHunterClient:
    """HeadHunter API client."""

    def __init__(
        self,
        settings: HeadHunterClientSettings,
        headers: dict[str, Any] = DEFAULT_CLIENT_HEADERS,
    ) -> None:
        """Initialize the client."""
        self._settings = settings
        self._headers = headers

    def _download(
        self,
        url: str,
        timeout: int = 60,
        params: dict | None = None,
        follow_redirects: bool = True,
    ) -> str:
        """Download page."""
        try:
            response = httpx.get(
                url,
                headers=self._headers,
                params=params,
                timeout=timeout,
                follow_redirects=follow_redirects,
            )
            response.raise_for_status()
            return response.text

        except httpx.HTTPStatusError as exc:
            raise HeadHunterDownloadPageError(
                f"HTTP error {exc.response.status_code} for {url}"
            ) from exc
        except httpx.RequestError as exc:
            # Ловим таймауты, обрывы связи, DNS-ошибки
            raise HeadHunterDownloadPageError(
                f"Network error while downloading {url}: {exc}"
            ) from exc

    def get_vacancies_from_search_page(
        self,
        keywords: list[str],
        page: int = 0,
        per_page: int = 10,
    ) -> list[VacancySearchParsingEntity]:
        """Fetch vacancies using required OAuth authentication."""
        vacancies_list: list[VacancySearchParsingEntity] = []

        for keyword in keywords:
            for num_page in range(page, per_page):
                params: dict[str, str | int] = {
                    "text": keyword,
                    "page": num_page,
                }

                html_content: str = self._download(
                    url=self._settings.base_url,
                    params=params,
                    timeout=self._settings.timeout_request,
                    follow_redirects=self._settings.follow_redirects,
                )
                try:
                    extend_parsed_vacancies_list = parsing_search_page(html_content)
                except Exception as exc:
                    raise HeadHunterSearchPageParsingError(
                        f"Error while parsing search page: {exc}"
                    ) from exc

                vacancies_list.extend(extend_parsed_vacancies_list)

                log.info(f"Awaiting ... {self._settings.time_delay} seconds")

                sleep(self._settings.time_delay)

        return vacancies_list

    def get_vacancy(self, url: str) -> VacancyParsingEntity:
        """Fetch and parse a single vacancy page."""
        html_content = self._download(
            url=url,
            follow_redirects=self._settings.follow_redirects,
            timeout=self._settings.timeout_request,
        )

        try:
            return parse_vacancy_page(html_content=html_content, url=url)
        except Exception as exc:
            raise HeadHunterVacancyPageParsingError(
                f"Error while parsing vacancy page {url}: {exc}"
            ) from exc
