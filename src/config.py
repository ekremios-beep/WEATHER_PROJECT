# src/config.py
"""
Application configuration module.

Loads and validates settings from environment variables (.env supported).
Includes security hardening and pylint-friendly caching.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Optional
from functools import lru_cache

from dotenv import load_dotenv

from .utils.logger import get_logger


LOGGER = get_logger()


def _sanitize_env(value: str) -> str:
    """Remove potentially dangerous characters such as newline injection."""
    return value.replace("\n", "").replace("\r", "").strip()


@dataclass(frozen=True)
class Settings:
    """Immutable application settings loaded from environment variables."""

    openweather_api_key: str
    mongo_uri: str

    smtp_host: str
    smtp_port: int
    smtp_user: str
    smtp_password: str
    from_email: str

    cities_file_path: Optional[str] = None

    @staticmethod
    def _get(
        name: str,
        *,
        required: bool = True,
        default: Optional[str] = None,
    ) -> Optional[str]:
        """Fetch and validate a single environment variable."""
        value = os.getenv(name, default)

        if value is None or value.strip() == "":
            if required:
                LOGGER.error("Missing required environment variable: %s", name)
                raise ValueError(f"Environment variable '{name}' is required but missing.")
            return default

        cleaned = _sanitize_env(value)

        if cleaned == "":
            LOGGER.error("Environment variable '%s' contains only whitespace.", name)
            raise ValueError(f"Environment variable '{name}' is invalid (only whitespace).")

        return cleaned

    @classmethod
    def from_env(cls) -> "Settings":
        """Load and validate full settings from environment variables."""
        load_dotenv()

        openweather_api_key = cls._get("OPENWEATHER_API_KEY")
        mongo_uri = cls._get("MONGO_URI")

        smtp_host = cls._get("SMTP_HOST")
        smtp_port_str = cls._get("SMTP_PORT", required=False, default="587")
        smtp_user = cls._get("SMTP_USER")
        smtp_password = cls._get("SMTP_PASSWORD")
        from_email = cls._get("FROM_EMAIL")

        try:
            smtp_port = int(smtp_port_str)
            if smtp_port <= 0:
                raise ValueError
        except ValueError as exc:
            LOGGER.error("Invalid SMTP_PORT value: %s", smtp_port_str)
            raise ValueError("Environment variable 'SMTP_PORT' must be a positive integer.") from exc

        cities_file_path = cls._get("CITIES_FILE_PATH", required=False, default=None)

        LOGGER.info("Configuration loaded successfully.")

        return cls(
            openweather_api_key=openweather_api_key,
            mongo_uri=mongo_uri,
            smtp_host=smtp_host,
            smtp_port=smtp_port,
            smtp_user=smtp_user,
            smtp_password=smtp_password,
            from_email=from_email,
            cities_file_path=cities_file_path,
        )


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return a cached Settings instance without using globals (Pylint-clean)."""
    LOGGER.debug("Initializing settings through LRU cache...")
    return Settings.from_env()
