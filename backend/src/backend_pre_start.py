import asyncio
import logging

from sqlalchemy import select
from tenacity import (
    before_log,
    before_sleep_log,
    retry,
    stop_after_attempt,
    stop_after_delay,
    wait_fixed,
)

from src.core.database import DB_HANDLER

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

MAX_RETRIES: int = 60
WAIT_SECONDS: int = 5
AFTER_DELAY: int = 300  # 5 minutes


@retry(
    stop=(stop_after_attempt(MAX_RETRIES) | stop_after_delay(AFTER_DELAY)),
    wait=wait_fixed(WAIT_SECONDS),
    before=before_log(log, logging.INFO),
    before_sleep=before_sleep_log(log, logging.WARNING),
)
async def init() -> None:
    """Initialize test database connection."""
    try:
        async with DB_HANDLER.get_session() as session:
            await session.execute(select(1))

    except Exception:
        log.exception("Database connection check failed")
        raise


def main() -> None:
    """Run before the uvicorn server starts."""
    log.info("Initializing service")
    asyncio.run(init())
    log.info("Service finished initializing")


if __name__ == "__main__":
    main()
