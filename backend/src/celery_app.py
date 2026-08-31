from datetime import timedelta

from celery import Celery

from src.core.config import init_celery_sentry

init_celery_sentry()

celery_app = Celery("worker")

celery_app.config_from_object("src.core.config.celeryconfig")

celery_app.autodiscover_tasks(["src.modules", "src.notifications"])

celery_app.conf.beat_schedule = {
    "every-5-seconds": {
        "task": "src.notifications.tasks.send_test_task",
        "schedule": timedelta(seconds=5),
        "args": ["Project is testing message!"],
    },
}
