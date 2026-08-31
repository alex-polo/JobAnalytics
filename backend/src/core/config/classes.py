import os
from pathlib import Path
from typing import Literal

from pydantic import (
    BaseModel,
    HttpUrl,
    PostgresDsn,
    SecretStr,
    computed_field,
)
from pydantic_settings import BaseSettings, SettingsConfigDict

type LogLevel = Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
type UvicornLoop = Literal["auto", "asyncio", "uvloop"]
type UvicornHTTP = Literal["auto", "h11", "httptools"]
type UvicornLifespan = Literal["auto", "on", "off"]


class BaseConfiguration(BaseSettings):
    """Base settings configuration class."""

    model_config = SettingsConfigDict(
        env_file=os.getenv("ENV_FILE", ".env.local"),
        env_file_encoding="utf-8",
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="BACKEND__",
        frozen=True,
        extra="ignore",
    )


class LoggingSettings(BaseModel):
    """Logging settings configuration."""

    log_level: LogLevel = "INFO"
    log_format: str = "%(asctime)s %(levelname)6s %(name)s: %(message)s"
    log_date_format: str = "%Y-%m-%d %H:%M:%S"
    sentry_dsn: HttpUrl | str = ""
    sentry_traces_sample_rate: float = 1.0
    sentry_log_level: LogLevel = "INFO"


class ProjectSettings(BaseModel):
    """Project settings configuration."""

    project_name: str
    description: str
    docs_url: str = "/docs"
    openapi_url: str = "/docs/openapi.json"
    redoc_url: str = "/re-docs"

    @property
    def title(self) -> str:
        """Return project title."""
        return f"{self.project_name} - Swagger UI"


class ApiV1Prefix(BaseModel):
    """API v1 prefix configuration."""

    prefix: str = "/v1"


class ApiPrefix(BaseModel):
    """API prefix configuration."""

    prefix: str = "/api"
    v1: ApiV1Prefix = ApiV1Prefix()


class DatabaseSettings(BaseModel):
    """Database settings configuration."""

    host: str
    port: int
    user: str
    user_password: SecretStr
    db_name: str
    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 50
    max_overflow: int = 10
    pool_pre_ping: bool = True
    pool_recycle: int = 3600
    autoflush: bool = False
    autocommit: bool = False
    expire_on_commit: bool = False

    naming_convention: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_N_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }

    @computed_field  # type: ignore[prop-decorator]
    @property
    def database_uri(self) -> PostgresDsn:
        """Get PostgreSQL DSN."""
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            username=self.user,
            password=self.user_password.get_secret_value(),
            host=self.host,
            port=self.port,
            path=self.db_name,
        )


class ServerSettings(BaseModel):
    """Base server settings."""

    host: str = "0.0.0.0"  # noqa: S104
    port: int = 8000
    log_level: LogLevel = "INFO"


class CORSSettings(BaseModel):
    """CORS settings configuration."""

    allow_credentials: bool = False
    allow_headers: list[str] = ["Content-Type", "Authorization"]
    allow_origins: list[str] = []
    allow_methods: list[str] = [
        "GET",
        "POST",
        "PUT",
        "DELETE",
        "OPTIONS",
        "PATCH",
        "HEAD",
    ]


class GunicornSettings(ServerSettings):
    """Gunicorn settings configuration."""

    workers: int = 1
    timeout: int = 60
    worker_class: str = "uvicorn.workers.UvicornWorker"
    access_log: str = "-"
    error_log: str = "-"

    # Graceful shutdown
    graceful_timeout: int = 30

    # Keep-alive
    keepalive: int = 5

    # Memory leak protection
    max_requests: int = 1000
    max_requests_jitter: int = 50


class UvicornSettings(ServerSettings):
    """Uvicorn settings configuration."""

    reload: bool = True
    loop: UvicornLoop = "auto"
    http: UvicornHTTP = "auto"
    lifespan: UvicornLifespan = "auto"
    access_log: bool = True
    use_colors: bool = True


class AuthSettings(BaseModel):
    """Auth settings configuration."""

    prefix: str = "/auth"
    token_url: str = "/api/v1/auth/login"  # noqa: S105
    cookie_name: str = "refresh_token"
    cookie_path: str = "/api"
    cookie_domain: str | None = None
    cookie_secure: bool = True
    cookie_samesite: Literal["lax", "strict", "none"] = "lax"
    jwt_access_token_expire_minutes: int = 5
    jwt_refresh_token_expire_days: int = 30
    jwt_private_key_path: Path
    jwt_public_key_path: Path

    @property
    def cookie_max_age(self) -> int:
        """Get cookie max age."""
        return self.jwt_refresh_token_expire_days * 24 * 3600

    @property
    def private_key(self) -> str:
        """Get private key."""
        return self.jwt_private_key_path.read_text(encoding="utf-8")

    @property
    def public_key(self) -> str:
        """Get public key."""
        return self.jwt_public_key_path.read_text(encoding="utf-8")


class RootUserSettings(BaseModel):
    """Admin settings configuration."""

    email: str
    password: SecretStr
    should_create: bool = False


class RedisSettings(BaseModel):
    """Redis settings configuration."""

    host: str = "redis"
    port: int = 6379
    max_connections: int = 10
    password: SecretStr
    db: int = 0
    result_db: int = 1
    socket_timeout: int = 5
    socket_connect_timeout: int = 5
    retry_on_timeout: bool = True
    ssl: bool = False

    @property
    def celery_broker_url(self) -> str:
        """Get Redis broker URL for Celery."""
        return f"redis://:{self.password.get_secret_value()}@{self.host}:{self.port}/{self.db}"

    @property
    def celery_result_backend_url(self) -> str:
        """Get Redis result backend URL for Celery."""
        return f"redis://:{self.password.get_secret_value()}@{self.host}:{self.port}/{self.result_db}"


class AppSettings(BaseConfiguration):
    """Server settings configuration."""

    ENVIRONMENT: Literal["local", "staging", "development", "production"]
    DOMAIN: str
    PROJECT: ProjectSettings
    DATABASE: DatabaseSettings
    REDIS: RedisSettings
    ROOT_USER: RootUserSettings
    AUTH: AuthSettings
    API_PREFIX: ApiPrefix = ApiPrefix()
    LOGGING: LoggingSettings = LoggingSettings()
    GUNICORN: GunicornSettings = GunicornSettings()
    UVICORN: UvicornSettings | None = None
    CORS: CORSSettings = CORSSettings()
