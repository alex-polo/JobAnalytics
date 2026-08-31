from logging import Formatter
from typing import TYPE_CHECKING

from gunicorn.glogging import Logger

from src.core.config import APP_SETTINGS

if TYPE_CHECKING:
    from gunicorn.config import Config


class GunicornLogger(Logger):
    """Custom Gunicorn logger."""

    def setup(self, cfg: Config) -> None:
        """Setup Gunicorn logger."""
        super().setup(cfg)

        log_format = Formatter(
            fmt=APP_SETTINGS.LOGGING.log_format,
            datefmt=APP_SETTINGS.LOGGING.log_date_format,
        )

        self._set_handler(  # type: ignore[attr-defined]
            log=self.access_log,
            output=cfg.accesslog,
            fmt=log_format,
        )

        self._set_handler(  # type: ignore[attr-defined]
            log=self.error_log,
            output=cfg.errorlog,
            fmt=log_format,
        )
