from unittest.mock import Mock

import pytest

from src.core.config.classes import HeadHunterClientSettings
from src.plugins.headhunter.client import HeadHunterClient


@pytest.fixture
def mock_settings() -> Mock:
    """Mock settings for HeadHunterClient."""
    settings = Mock(spec=HeadHunterClientSettings)
    settings.base_url = "https://hh.ru/search/vacancy"
    settings.timeout_request = 30
    settings.time_delay = 0.1
    settings.follow_redirects = True
    return settings


@pytest.fixture
def client(mock_settings: Mock) -> HeadHunterClient:
    """Fixture for HeadHunterClient."""
    return HeadHunterClient(settings=mock_settings)
