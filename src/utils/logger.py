# src/utils/logger.py
"""
Centralized logging configuration for the Weather Project.

Includes:
- Rotating file logs
- Console logs
- .env-based log level control
- Safe, idempotent logger initialization
"""

from __future__ import annotations

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
import os


_LOGGER_NAME = "weather_project"


def _get_log_level() -> int:
    """
    Determine log level from environment variable LOG_LEVEL.
    Supports: DEBUG, INFO, WARNING, ERROR, CRITICAL.
    Defaults to INFO.
    """
    level = os.getenv("LOG_LEVEL", "INFO").upper()
    return getattr(logging, level, logging.INFO)


def _configure_logger() -> logging.Logger:
    """Configure and return the project logger."""
    logger = logging.getLogger(_LOGGER_NAME)

    if logger.handlers:
        # Logger already configured → avoid duplicate handlers
        return logger

    # Set log level dynamically
    logger.setLevel(_get_log_level())

    # Structured log format
    log_format = (
        "%(asctime)s - %(levelname)s - %(module)s:%(lineno)d - %(message)s"
    )
    formatter = logging.Formatter(log_format)

    # Base project directory
    base_dir = Path(__file__).resolve().parent.parent
    logs_dir = base_dir / "logs"
    logs_dir.mkdir(exist_ok=True)

    # File handler (rotating)
    file_handler = RotatingFileHandler(
        logs_dir / "app.log",
        maxBytes=1_000_000,
        backupCount=3,
        encoding="utf-8",
        delay=True,  # open file lazily → safer & faster
    )
    file_handler.setLevel(_get_log_level())
    file_handler.setFormatter(formatter)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(_get_log_level())
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    logger.debug("Logger configured successfully with level: %s", _get_log_level())
    return logger


def get_logger() -> logging.Logger:
    """Return the configured logger."""
    return _configure_logger()
