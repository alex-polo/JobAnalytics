"""Celery tasks for vacancy discovery and download.

Three tasks form the pipeline:

* ``discover_vacancies`` -- walk all sources, discover vacancies for
  each keyword, register raw vacancies.
* ``download_raw_vacancies`` -- pick a batch of raw vacancies in
  ``NOT_DOWNLOADED`` state and spawn a download task for each.
* ``download_single_vacancy`` -- download a single raw vacancy
  through the source plugin and persist the result.

Tasks are sync (Celery entrypoints) and delegate to ``async def``
inner functions run via ``asyncio.run``. Each task opens its own DB
session(s); sessions do not cross task boundaries.
"""

import asyncio
import logging
from typing import Any

from celery import shared_task

from src.core.database.engine import DB_HANDLER
from src.modules.discovery_vacancy.application.factory import (
    DiscoveryServiceFactory,
)
from src.modules.discovery_vacancy.application.scheduler_service import (
    SchedulerService,
)
from src.modules.sources.application.services import SourcesService
from src.plugins.exceptions import BasePluginError

log = logging.getLogger(__name__)

#: How many raw vacancies to enqueue per download run.
DOWNLOADS_PER_RUN = 100


@shared_task()
def discover_vacancies() -> dict[str, Any]:
    """Discover vacancies for every source from the scheduler.

    Per-source session is required: a failure inside
    ``process_source`` rolls back that session and expires its ORM
    objects, so reusing it for the next source would raise
    ``MissingGreenlet``.

    Returns:
        Metrics: ``vacancies_found``, ``error_sources``,
        ``sessions_args``.
    """
    log.info("Task discover_vacancies started")

    async def inner() -> dict[str, Any]:
        metrics = {
            "vacancies_found": 0,
            "error_sources": [],
            "sessions_args": [],
        }

        # --- Load sources in a dedicated short-lived session ---
        async with DB_HANDLER.async_session_maker() as db_session:
            sources_service = SourcesService(session=db_session)
            scheduler_service = SchedulerService(sources_service)
            sources_to_process = await scheduler_service.get_sources_to_process()

        log.info("Sources to process: %s", len(sources_to_process))

        # --- Process each source in its own session ---
        for source_id, source_code in sources_to_process:
            log.info(
                "Processing source, id: %s, code: %s",
                source_id,
                source_code,
            )

            async with DB_HANDLER.async_session_maker() as db_session:
                factory = DiscoveryServiceFactory(db_session=db_session)
                discovery_service = factory.create_discovery_service()

                try:
                    (
                        count_vacancies,
                        session_args,
                    ) = await discovery_service.process_source(
                        source_id=source_id,
                        source_code=source_code,
                    )

                    metrics["vacancies_found"] += count_vacancies
                    metrics["sessions_args"].append(session_args)

                    log.info(
                        "Source processed, id: %s, vacancies: %s",
                        source_id,
                        count_vacancies,
                    )

                except Exception as e:
                    metrics["error_sources"].append({
                        "source_id": source_id,
                        "source_name": source_code,
                        "error": str(e),
                    })

                    log.exception("Error on source id=%s", source_id)

                    # Original session was rolled back; use a new one
                    # to persist the error.
                    try:
                        async with DB_HANDLER.async_session_maker() as err_session:
                            err_factory = DiscoveryServiceFactory(
                                db_session=err_session
                            )
                            err_service = err_factory.create_discovery_service()
                            await err_service.registry_error_discovery_session(
                                source_id=source_id,
                                error=e,
                            )
                        log.info(
                            "Error recorded for source, id: %s",
                            source_id,
                        )
                    except Exception:
                        log.exception(
                            "Failed to record error for source id=%s",
                            source_id,
                        )

        log.info(
            "Task discover_vacancies finished, vacancies_found: %s, error_sources: %s",
            metrics["vacancies_found"],
            len(metrics["error_sources"]),
        )
        return metrics

    return asyncio.run(inner())


@shared_task()
def download_raw_vacancies() -> dict[str, Any]:
    """Spawn download tasks for pending raw vacancies.

    Selects up to ``DOWNLOADS_PER_RUN`` raw vacancies in
    ``NOT_DOWNLOADED`` state and enqueues one download task per
    vacancy. The DB session is closed before enqueueing, so broker
    I/O does not happen while a pool connection is held.

    Returns:
        Metrics: ``selected_vacancies``, ``spawned_tasks``.
    """
    log.info("Task download_raw_vacancies started")

    async def spawned_download_tasks() -> dict[str, Any]:
        async with DB_HANDLER.async_session_maker() as db_session:
            factory = DiscoveryServiceFactory(db_session=db_session)
            discovery_service = factory.create_discovery_service()
            vacancies_ids: list[int] = await discovery_service.get_vacancies_ids(
                limit=DOWNLOADS_PER_RUN
            )

        count_vacancies = len(vacancies_ids)
        log.info("Found %s vacancies for download", count_vacancies)

        metrics = {
            "selected_vacancies": count_vacancies,
            "spawned_tasks": 0,
        }

        for vacancy_id in vacancies_ids:
            download_single_vacancy.delay(vacancy_id=vacancy_id)
            metrics["spawned_tasks"] += 1
            log.info("Spawned download task, vacancy_id: %s", vacancy_id)

        log.info(
            "Task download_raw_vacancies finished, selected: %s, spawned: %s",
            metrics["selected_vacancies"],
            metrics["spawned_tasks"],
        )
        return metrics

    return asyncio.run(spawned_download_tasks())


@shared_task()
def download_single_vacancy(vacancy_id: int) -> dict[str, Any]:
    """Download a single raw vacancy and persist its content.

    HTTP happens outside any transaction. ``BasePluginError`` is an
    expected business failure: the service already marked the
    vacancy as ``ERROR`` in the DB, and the task returns
    ``success=False`` so Celery keeps the task succeeded and Sentry
    stays quiet. Other exceptions propagate and fail the task.

    Returns:
        ``{"success": True, "vacancy_id": int}`` on success, or
        ``{"success": False, "vacancy_id": int, "error": str}`` on a
        plugin error.
    """
    log.info("Task download_single_vacancy started, vacancy_id: %s", vacancy_id)

    async def inner() -> dict[str, Any]:
        async with DB_HANDLER.async_session_maker() as db_session:
            service = DiscoveryServiceFactory(
                db_session=db_session,
            ).create_discovery_service()

            try:
                await service.download_raw_vacancy(
                    raw_vacancy_id=vacancy_id,
                )
            except BasePluginError as e:
                log.warning(
                    "Plugin error on download, vacancy_id: %s, "
                    "error_type: %s, error: %s",
                    vacancy_id,
                    type(e).__name__,
                    e,
                )
                return {
                    "success": False,
                    "vacancy_id": vacancy_id,
                    "error": f"{type(e).__name__}: {e!s}",
                }

            log.info(
                "Vacancy downloaded successfully, vacancy_id: %s",
                vacancy_id,
            )
            return {"success": True, "vacancy_id": vacancy_id}

    return asyncio.run(inner())
