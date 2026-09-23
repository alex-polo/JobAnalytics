"""Automatically imports all models."""

import contextlib
import importlib
import pkgutil
from pathlib import Path

from src.core.database import Base


def discover_models() -> None:
    """Automatically imports all models from moduless."""
    modules_path = Path(__file__).parent.parent.parent / "modules"

    for package_info in pkgutil.iter_modules([str(modules_path)]):
        if package_info.ispkg:
            with contextlib.suppress(ImportError):
                importlib.import_module(
                    f"src.modules.{package_info.name}.infrastructure.models"
                )


discover_models()

Base.registry.configure()
