import logging

from src.notifications.tasks import send_test_task

log = logging.getLogger(__name__)


def test_test_taks() -> None:
    """Test send test task."""
    result = send_test_task.delay("Hello, Test celery!")
    assert result.ready()
    assert result.result == "Test task: Hello, Test celery!"
