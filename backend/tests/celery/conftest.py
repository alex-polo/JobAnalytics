from typing import TYPE_CHECKING

import pytest

from src.celery_app import celery_app

if TYPE_CHECKING:
    from collections.abc import Generator


@pytest.fixture(scope="package", autouse=True)
def setup_test_celery() -> Generator[None]:
    """Setup Celery for testing."""
    celery_app.conf.task_always_eager = True
    celery_app.conf.task_eager_propagates = True

    yield

    celery_app.conf.task_always_eager = False
    celery_app.conf.task_eager_propagates = False
