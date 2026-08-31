from src.core.config import APP_SETTINGS
from src.core.gunicorn import GunicornApplication, get_gunicorn_options
from src.main import app as main_app


def main() -> None:
    """Starting FastAPI-application in production mode with Gunicorn."""
    options: dict[str, str] = get_gunicorn_options(
        host=APP_SETTINGS.GUNICORN.host,
        port=APP_SETTINGS.GUNICORN.port,
        timeout=APP_SETTINGS.GUNICORN.timeout,
        workers=APP_SETTINGS.GUNICORN.workers,
        worker_class=APP_SETTINGS.GUNICORN.worker_class,
        log_level=APP_SETTINGS.GUNICORN.log_level,
        access_log=APP_SETTINGS.GUNICORN.access_log,
        error_log=APP_SETTINGS.GUNICORN.error_log,
        graceful_timeout=APP_SETTINGS.GUNICORN.graceful_timeout,
        keepalive=APP_SETTINGS.GUNICORN.keepalive,
        max_requests=APP_SETTINGS.GUNICORN.max_requests,
        max_requests_jitter=APP_SETTINGS.GUNICORN.max_requests_jitter,
    )

    GunicornApplication(app=main_app, options=options).run()


if __name__ == "__main__":
    main()
