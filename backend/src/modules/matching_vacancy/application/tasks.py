import asyncio
import logging
from typing import Any

from src.celery_app import celery_app
from src.core.database.engine import DB_HANDLER
from src.plugins.llm.exceptions import LLMTimeoutError

from .factory import MatchingServiceFactory

log = logging.getLogger(__name__)


@celery_app.task(name="matching.dispatch_pending")
def matching_dispatch_pending() -> dict[str, Any]:
    """Dispatch matching task."""

    async def _run() -> dict[str, Any]:
        """Inner matching task."""
        metrics: dict[str, str | int] = {
            "success": False,
        }
        log.info("Start dispatch matching task")
        async with DB_HANDLER.async_session_maker() as db_session:
            factory_matching_service = MatchingServiceFactory(db_session=db_session)
            matching_service = factory_matching_service.create_service()
            try:
                queue_list = await matching_service.queue_claim_batch(limit=5)
            except Exception as e:
                log.exception("Error on dispatch matching task, error: %s", e)
                raise
        for queue_item in queue_list:
            log.info("Dispatch matching task, queue_id: %s", queue_item.id)
            run_matching.delay(queue_id=queue_item.id)

        metrics["dispatched_tasks"] = len(queue_list)
        metrics["success"] = True

        return metrics

    return asyncio.run(_run())


@celery_app.task(
    name="matching.run",
    autoretry_for=(LLMTimeoutError,),
    retry_backoff=True,
    max_retries=3,
    acks_late=True,
)
def run_matching(queue_id: int) -> dict[str, Any]:
    """Run matching task."""
    log.info("matching")

    async def _run() -> dict[str, Any]:
        """Inner matching task."""
        log.info("Start matching task, queue_id: %s", queue_id)
        metrics = {
            "queue_id": queue_id,
            "success": False,
        }
        async with DB_HANDLER.async_session_maker() as db_session:
            try:
                factory_matching_service = MatchingServiceFactory(db_session=db_session)
                matching_service = factory_matching_service.create_service()
                await matching_service.match(queue_id=queue_id)

            except LLMTimeoutError as e:
                log.exception("LLM timeout error: %s", e)
                raise

            except Exception as e:
                log.error("Matching task failed, queue_id: %s, error: %s", queue_id, e)
                factory_matching_service = MatchingServiceFactory(db_session=db_session)
                matching_service = factory_matching_service.create_service()
                await matching_service.mark_failed(queue_id, error=e)
                raise

            else:
                await matching_service.mark_done(queue_id=queue_id)
                metrics["success"] = True
        return metrics

    return asyncio.run(_run())
