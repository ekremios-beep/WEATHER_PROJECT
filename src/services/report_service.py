# src/services/report_service.py
"""Service for building human-readable weather reports."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Dict

from ..utils.logger import get_logger


LOGGER = get_logger()


def _safe_get(data: Dict[str, Any], key: str, default: str = "?") -> Any:
    """Safely extract values from nested dictionaries."""
    value = data.get(key, default)
    if value == default:
        LOGGER.warning("Missing expected field '%s' in weather API data.", key)
    return value


def _sanitize_text(text: str) -> str:
    """Sanitize text to avoid newline injection or malformed output."""
    return text.replace("\n", " ").replace("\r", " ").strip()


class ReportService:
    """Generates plain-text weather reports."""

    @staticmethod
    def build_daily_report(city_name: str, data: Dict[str, Any]) -> str:
        """Build a robust daily weather report for the given city."""
        now_str = datetime.now().strftime("%d.%m.%Y %H:%M")

        # Basic groups
        main = data.get("main", {})
        wind = data.get("wind", {})
        weather_list = data.get("weather", [])

        # Weather description
        description = "Bilinmiyor"
        if isinstance(weather_list, list) and weather_list:
            first = weather_list[0]
            if isinstance(first, dict):
                description = first.get("description", "Bilinmiyor")
            else:
                LOGGER.warning("Weather list entry is not a dict: %r", first)
        else:
            LOGGER.warning("Weather list missing or invalid.")

        description = _sanitize_text(str(description))

        # Safe extraction of fields
        temp = _safe_get(main, "temp")
        feels_like = _safe_get(main, "feels_like")
        temp_min = _safe_get(main, "temp_min")
        temp_max = _safe_get(main, "temp_max")
        humidity = _safe_get(main, "humidity")
        pressure = _safe_get(main, "pressure")
        wind_speed = _safe_get(wind, "speed")
        wind_deg = _safe_get(wind, "deg")

        city_clean = _sanitize_text(city_name)

        lines = [
            f"WEATHER REPORT (Daily) - {now_str}",
            "-" * 40,
            f"Province: {city_clean}",
            f"Condition: {description}",
            f"Temperature: {temp}°C (Hissedilen: {feels_like}°C)",
            f"Minimum / Maximum: {temp_min}°C / {temp_max}°C",
            f"Humidity: {humidity}%",
            f"Pressure: {pressure} hPa",
            f"Wind Speed: {wind_speed} m/s, Yön: {wind_deg}°",
            "-" * 40,
            "We wish you a good day.",
        ]

        LOGGER.info("Daily weather report built for city '%s'.", city_clean)

        return "\n".join(lines)
