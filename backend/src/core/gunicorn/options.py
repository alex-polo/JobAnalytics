def get_gunicorn_options(
    host: str,
    port: int,
    timeout: int,
    workers: int,
    worker_class: str,
    log_level: str,
    access_log: str,
    error_log: str,
    graceful_timeout: int = 30,
    keepalive: int = 5,
    max_requests: int = 1000,
    max_requests_jitter: int = 50,
) -> dict[str, str]:
    """Get Gunicorn application options."""
    return {
        "bind": f"{host}:{port}",
        "timeout": str(timeout),
        "worker_class": worker_class,
        "workers": str(workers),
        "loglevel": log_level,
        "access_log": access_log,
        "error_log": error_log,
        "graceful_timeout": str(graceful_timeout),
        "keepalive": str(keepalive),
        "max_requests": str(max_requests),
        "max_requests_jitter": str(max_requests_jitter),
        "logger_class": "src.core.gunicorn.logger.GunicornLogger",
    }
