# src/services/database_service.py
"""Service responsible for persisting weather data into MongoDB."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Dict

from pymongo import MongoClient, errors

from ..config import get_settings
from ..utils.exceptions import DatabaseError
from ..utils.logger import get_logger


LOGGER = get_logger()


def sanitize_mongo_uri(uri: str) -> str:
    """Remove newline injection or whitespace from Mongo URI."""
    return uri.replace("\n", "").replace("\r", "").strip()


class DatabaseService:
    """MongoDB wrapper for saving weather reports."""

    def __init__(self) -> None:
        self._settings = get_settings()
        mongo_uri = sanitize_mongo_uri(self._settings.mongo_uri)

        try:
            self._client = MongoClient(
                mongo_uri,
                serverSelectionTimeoutMS=5000,
            )
            # Test connection
            self._client.admin.command("ping")
            LOGGER.info("Connected to MongoDB successfully.")
        except errors.PyMongoError as exc:
            LOGGER.error("Could not connect to MongoDB using URI '%s': %s", mongo_uri, exc)
            raise DatabaseError(
                "Database connection failed. Check MONGO_URI and server status."
            ) from exc

        self._db = self._client["weather_project"]
        self._collection = self._db["weather_reports"]

    def save_weather_report(self, city_name: str, raw_data: Dict[str, Any]) -> None:
        """Insert a single weather report document.

        Raises:
            DatabaseError: If insert fails.
        """
        if not isinstance(raw_data, dict):
            raise DatabaseError("Weather data must be a dictionary.")

        document = {
            "city": city_name,
            "timestamp": datetime.utcnow(),
            "raw_data": raw_data,
        }

        try:
            self._collection.insert_one(document)
            LOGGER.info("Weather report saved for city %s", city_name)
        except errors.AutoReconnect as exc:
            # Retry once if Mongo temporarily drops connection
            LOGGER.warning("MongoDB AutoReconnect: retrying insert... %s", exc)
            try:
                self._collection.insert_one(document)
            except errors.PyMongoError as exc2:
                LOGGER.error("Retry failed while inserting weather report: %s", exc2)
                raise DatabaseError("Database insert retry failed.") from exc2
        except errors.PyMongoError as exc:
            LOGGER.error("Failed to insert weather report: %s", exc)
            raise DatabaseError("Failed to insert weather report.") from exc
