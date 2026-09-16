from unittest.mock import Mock, patch

import httpx
import pytest

from src.plugins.headhunter import (
    HeadHunterClient,
)
from src.plugins.headhunter.exceptions import (
    HeadHunterDownloadPageError,
    HeadHunterSearchPageParsingError,
)
from src.plugins.headhunter.schemas import VacancySearchParsingEntity


class TestHeadHunterClientDownload:
    """Tests for _download method."""

    @patch("src.plugins.headhunter.client.httpx.get")
    def test_download_success(
        self,
        mock_get: Mock,
        client: HeadHunterClient,
    ) -> None:
        """Test successful page download."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = "<html>test</html>"
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        result = client._download("https://example.com")

        assert result == "<html>test</html>"
        mock_response.raise_for_status.assert_called_once()

    @patch("src.plugins.headhunter.client.httpx.get")
    def test_download_http_error(
        self,
        mock_get: Mock,
        client: HeadHunterClient,
    ) -> None:
        """Test HTTP error handling."""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.raise_for_status.side_effect = httpx.HTTPStatusError(
            "Not Found", request=Mock(), response=mock_response
        )
        mock_get.return_value = mock_response

        with pytest.raises(HeadHunterDownloadPageError, match="HTTP error 404"):
            client._download("https://example.com")

    @patch("src.plugins.headhunter.client.httpx.get")
    def test_download_network_error(
        self,
        mock_get: Mock,
        client: HeadHunterClient,
    ) -> None:
        """Test network error handling."""
        mock_get.side_effect = httpx.RequestError("Connection failed")

        with pytest.raises(HeadHunterDownloadPageError, match="Network error"):
            client._download("https://example.com")


class TestGetVacanciesFromSearchPage:
    """Tests for get_vacancies_from_search_page method."""

    @patch("src.plugins.headhunter.client.parsing_search_page")
    @patch.object(HeadHunterClient, "_download")
    def test_get_vacancies_success(
        self,
        mock_download: Mock,
        mock_parse: Mock,
        client: HeadHunterClient,
    ) -> None:
        """Test successful vacancy list parsing."""
        mock_download.return_value = "<html>search results</html>"
        mock_vacancies = [
            VacancySearchParsingEntity(
                title="Python Dev", url="https://hh.ru/vacancy/1"
            ),
            VacancySearchParsingEntity(
                title="Django Dev", url="https://hh.ru/vacancy/2"
            ),
        ]
        mock_parse.return_value = mock_vacancies

        result = client.get_vacancies_from_search_page(
            keywords=["python"],
            page=0,
            per_page=1,
        )

        assert len(result) == 2
        assert result[0].title == "Python Dev"

    @patch("src.plugins.headhunter.client.parsing_search_page")
    @patch.object(HeadHunterClient, "_download")
    def test_get_vacancies_handles_parsing_error(
        self,
        mock_download: Mock,
        mock_parse: Mock,
        client: HeadHunterClient,
    ) -> None:
        """Test that parsing errors are logged but don't break."""
        mock_download.return_value = "<html></html>"
        mock_parse.side_effect = Exception("Parse error")

        with pytest.raises(HeadHunterSearchPageParsingError):
            client.get_vacancies_from_search_page(
                keywords=["python"],
                page=0,
                per_page=1,
            )

    @patch("src.plugins.headhunter.client.parsing_search_page")
    @patch.object(HeadHunterClient, "_download")
    def test_get_vacancies_multiple_keywords(
        self,
        mock_download: Mock,
        mock_parse: Mock,
        client: HeadHunterClient,
    ) -> None:
        """Test parsing multiple keywords."""
        mock_download.return_value = "<html></html>"
        mock_vacancies = [
            VacancySearchParsingEntity(
                title="Vacancy",
                url="https://hh.ru/vacancy/test",
            )
        ]
        mock_parse.return_value = mock_vacancies

        result = client.get_vacancies_from_search_page(
            keywords=["python", "django"],
            page=0,
            per_page=1,
        )

        assert len(result) == 2
