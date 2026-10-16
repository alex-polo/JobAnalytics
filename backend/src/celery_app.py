from celery import Celery
from celery.schedules import crontab

from src.core.config import init_celery_sentry

init_celery_sentry()

celery_app = Celery("worker")

celery_app.config_from_object("src.core.config.celeryconfig")

celery_app.autodiscover_tasks([
    "src.modules",
    "src.notifications",
])

celery_app.conf.beat_schedule = {
    "dicovery-vacancy-from-sources-every-30-min": {
        "task": "src.modules.discovery_vacancy.application.tasks.discover_vacancies",
        "schedule": crontab(minute="*/15"),
    },
    "spawned-download-vacancy-task-every-1-min": {
        "task": "src.modules.discovery_vacancy.application.tasks.download_raw_vacancies",  # noqa: E501
        "schedule": crontab(minute="*/1"),
    },
}
