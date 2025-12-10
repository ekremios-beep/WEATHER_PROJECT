# src/services/weather_service.py
"""Service for fetching current weather data from OpenWeatherMap API."""

from __future__ import annotations

import time
from typing import Any, Dict

import requests

from ..config import get_settings
from ..utils.exceptions import WeatherApiError
from ..utils.logger import get_logger


LOGGER = get_logger()


def sanitize_query(query: str) -> str:
    """Remove dangerous or invalid characters from city query, but keep comma."""
    cleaned = query.replace("\n", "").replace("\r", "").strip()
    cleaned = "".join(ch for ch in cleaned if ch.isalnum() or ch in {" ", "-", "_", ","})
    return cleaned


class WeatherService:
    """Handles communication with the OpenWeatherMap API."""

    BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

    def __init__(self, max_retries: int = 3, retry_delay: float = 1.5) -> None:
        self._settings = get_settings()
        self._max_retries = max_retries
        self._retry_delay = retry_delay

    def get_current_weather(self, city_query: str, lang: str = "tr") -> Dict[str, Any]:
        """Fetch current weather for a given city with retry and sanitization."""
        safe_query = sanitize_query(city_query)

        params = {
            "q": safe_query,
            "appid": self._settings.openweather_api_key,
            "units": "metric",
            "lang": lang,
        }

        last_exception: Exception | None = None

        for attempt in range(1, self._max_retries + 1):
            try:
                response = requests.get(self.BASE_URL, params=params, timeout=10)

                if not response.ok:
                    LOGGER.warning(
                        "Weather API returned HTTP %s on attempt %d. Body: %s",
                        response.status_code,
                        attempt,
                        response.text[:200],
                    )

                    if 400 <= response.status_code < 500:
                        raise WeatherApiError(
                            f"Weather API client error: HTTP {response.status_code}"
                        )

                    raise WeatherApiError(
                        f"Weather API server error: HTTP {response.status_code}"
                    )

                try:
                    data = response.json()
                except ValueError as exc:
                    LOGGER.error(
                        "Weather API returned non-JSON response. Body: %s",
                        response.text[:200],
                    )
                    raise WeatherApiError("Invalid JSON from weather API.") from exc

                if not isinstance(data, dict):
                    LOGGER.error("Weather API returned non-object JSON: %r", data)
                    raise WeatherApiError("Unexpected weather API response type.")

                if "main" not in data or "weather" not in data:
                    LOGGER.error("Missing required keys in weather API response: %s", data)
                    raise WeatherApiError("Unexpected weather API response structure.")

                LOGGER.info("Successfully fetched weather for %s", safe_query)
                return data

            except Exception as exc:
                last_exception = exc

                LOGGER.warning(
                    "Attempt %d/%d to fetch weather failed: %s",
                    attempt, self._max_retries, exc
                )

                if attempt < self._max_retries:
                    delay = self._retry_delay * (2 ** (attempt - 1))
                    time.sleep(delay)

        # All attempts exhausted
        raise WeatherApiError(
            f"Weather API request failed after {self._max_retries} attempts: {last_exception}"
        ) from last_exception
