from typing import TYPE_CHECKING

from gunicorn.app.base import BaseApplication

if TYPE_CHECKING:
    from fastapi import FastAPI


class GunicornApplication(BaseApplication):
    """Custom Gunicorn application for running a FastAPI."""

    def __init__(self, app: FastAPI, options: dict[str, str]) -> None:
        """Initialize Gunicorn application."""
        self.options = options
        self.application = app
        super().__init__()

    @property
    def config_options(self) -> dict[str, str]:
        """Get Gunicorn configuration options."""
        return {
            key: value
            for key, value in self.options.items()
            if key.lower() in self.cfg.settings and value is not None
        }

    def load_config(self) -> None:
        """Load Gunicorn configuration from the options."""
        for key, value in self.config_options.items():
            self.cfg.set(key.lower(), value)

    def load(self) -> FastAPI:
        """Return the FastAPI application instance to be served.

        This method is called by Gunicorn during startup.

        Returns:
            The FastAPI app instance.
        """
        return self.application
