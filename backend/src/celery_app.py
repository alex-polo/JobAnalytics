from datetime import timedelta

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
    "discover-vacancy-overview-every-20-min": {
        "task": "discover.vacancy_overview",
        "schedule": crontab(minute="*/20"),
    },
    "discover-dispatch-pending-task-every-7-min": {
        "task": "discover.dispatch_pending",
        "schedule": crontab(minute="*/7"),
    },
    "matching-dispatch-pending-task-every-20-sec": {
        "task": "matching.dispatch_pending",
        "schedule": timedelta(seconds=20),
    },
}
