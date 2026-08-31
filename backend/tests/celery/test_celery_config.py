import logging

from celery import Celery

from src.celery_app import celery_app

log = logging.getLogger(__name__)


def test_task_is_registered() -> None:
    """Test that task is registered."""
    assert "src.notifications.tasks.send_test_task" in celery_app.tasks


def test_celery_app_initialization() -> None:
    """Test celery app initialization."""
    assert isinstance(celery_app, Celery)

    assert celery_app.conf.task_serializer == "json"
    assert celery_app.conf.result_serializer == "json"
    assert celery_app.conf.accept_content == ["json"]


# @pytest.mark.skip(reason="Этот тест пока не работает.")
def test_celery_app_config() -> None:
    """Test celery app configuration."""
    from src.core.config import APP_SETTINGS

    log.info(APP_SETTINGS.REDIS.celery_broker_url)

    assert celery_app.conf.broker_url == APP_SETTINGS.REDIS.celery_broker_url
    assert (
        celery_app.conf.result_backend == APP_SETTINGS.REDIS.celery_result_backend_url
    )

    assert celery_app.conf.broker_pool_limit == APP_SETTINGS.REDIS.max_connections
    assert celery_app.conf.enable_utc is True
