# Celery tasks
from .discovery_vacancy.application.tasks import discover_vacancies

__all__ = ("discover_vacancies",)
