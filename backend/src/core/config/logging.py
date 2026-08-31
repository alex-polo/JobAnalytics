import logging

import sentry_sdk
from sentry_sdk.integrations.celery import CeleryIntegration
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.logging import LoggingIntegration

from .settings import APP_SETTINGS


def setup_logging() -> None:
    """Apply logging configuration from APP_SETTINGS."""
    if APP_SETTINGS.LOGGING.sentry_dsn and APP_SETTINGS.ENVIRONMENT != "local":
        sentry_sdk.init(
            dsn=str(APP_SETTINGS.LOGGING.sentry_dsn),
            environment=APP_SETTINGS.ENVIRONMENT,
            traces_sample_rate=APP_SETTINGS.LOGGING.sentry_traces_sample_rate,
            enable_tracing=True,
            integrations=[
                FastApiIntegration(),
                LoggingIntegration(
                    level=logging.INFO,
                    event_level=getattr(logging, APP_SETTINGS.LOGGING.sentry_log_level),
                ),
            ],
        )

    logging.basicConfig(
        level=APP_SETTINGS.LOGGING.log_level,
        format=APP_SETTINGS.LOGGING.log_format,
        datefmt=APP_SETTINGS.LOGGING.log_date_format,
        force=True,
    )

    for logger in logging.Logger.manager.loggerDict.values():
        if isinstance(logger, logging.Logger):
            logger.setLevel(APP_SETTINGS.LOGGING.log_level)
            logger.propagate = True


def init_celery_sentry() -> None:
    """Apply logging configuration from APP_SETTINGS."""
    if APP_SETTINGS.LOGGING.sentry_dsn and APP_SETTINGS.ENVIRONMENT != "local":
        sentry_sdk.init(
            dsn=str(APP_SETTINGS.LOGGING.sentry_dsn),
            environment=APP_SETTINGS.ENVIRONMENT,
            traces_sample_rate=APP_SETTINGS.LOGGING.sentry_traces_sample_rate,
            enable_tracing=True,
            integrations=[
                CeleryIntegration(),
                LoggingIntegration(
                    level=logging.INFO,
                    event_level=getattr(logging, APP_SETTINGS.LOGGING.sentry_log_level),
                ),
            ],
        )
