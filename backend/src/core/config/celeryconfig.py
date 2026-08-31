from src.core.config.settings import APP_SETTINGS

# Broker and Result Backend URLs
broker_url = APP_SETTINGS.REDIS.celery_broker_url
result_backend = APP_SETTINGS.REDIS.celery_result_backend_url

# Serialization: Use JSON for tasks and results
task_serializer = "json"
result_serializer = "json"
accept_content = ["json"]
result_accept_content = ["json"]

# Timezone: Use UTC for consistent scheduling
timezone = "UTC"
enable_utc = True

# Reliability: Late ACKs ensure tasks aren't lost if worker crashes
task_acks_late = True
task_reject_on_worker_lost = True

# Concurrency: Each worker processes one task at a time
worker_prefetch_multiplier = 1

# Memory Leak Protection: Restart worker after N tasks
worker_max_tasks_per_child = 10

# Logging: Configure Celery worker output format
worker_hijack_root_logger = False
worker_log_format = APP_SETTINGS.LOGGING.log_format

# Broker Connection: Retry on startup and limit pool size
broker_connection_retry_on_startup = True
broker_pool_limit = APP_SETTINGS.REDIS.max_connections

# Broker Transport: Socket timeouts and retries
broker_transport_options = {
    "socket_timeout": APP_SETTINGS.REDIS.socket_timeout,
    "socket_connect_timeout": APP_SETTINGS.REDIS.socket_connect_timeout,
    "retry_on_timeout": APP_SETTINGS.REDIS.retry_on_timeout,
}

# SSL: Enable secure connections for Redis
broker_use_ssl = APP_SETTINGS.REDIS.ssl

# Results: Expire stored results after 1 hour
result_expires = 3600

# Result Backend Transport: Socket timeouts and retries
result_backend_transport_options = {
    "socket_timeout": APP_SETTINGS.REDIS.socket_timeout,
    "socket_connect_timeout": APP_SETTINGS.REDIS.socket_connect_timeout,
    "retry_on_timeout": APP_SETTINGS.REDIS.retry_on_timeout,
}

# Result Backend SSL: Enable secure connections for result backend
redis_backend_use_ssl = APP_SETTINGS.REDIS.ssl


# Celery Beat: Scheduler for periodic tasks
beat_scheduler = "celery.beat:PersistentScheduler"
# beat_schedule_filename = "/app/celerybeat-schedule"  # noqa: ERA001
beat_schedule_filename = "./celerybeat-schedule"
beat_max_loop_interval = 5  # Check for new tasks every 3 seconds
beat_sync_every = 10  # Sync schedule to disk every 10 seconds
