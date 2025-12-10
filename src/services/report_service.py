# src/services/report_service.py
"""Service for building human-readable weather reports."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Dict

from ..utils.logger import get_logger


LOGGER = get_logger()


def _sanitize_text(text: str) -> str:
    """Sanitize text to avoid newline injection or malformed output."""
    return text.replace("\n", " ").replace("\r", " ").strip()


class ReportService:
    """Generates plain-text weather reports."""

    @staticmethod
    def _validate_required_fields(data: Dict[str, Any]) -> None:
        """Validate presence of all required fields, otherwise raise KeyError."""

        # Validate main block
        required_main = ["temp", "feels_like", "temp_min", "temp_max", "humidity", "pressure"]

        if "main" not in data:
            raise KeyError("Missing 'main' section")

        for key in required_main:
            if key not in data["main"]:
                LOGGER.warning("Missing expected field '%s' in weather API data.", key)
                raise KeyError(f"Missing field '{key}' in main")

        # Validate wind block
        if "wind" not in data:
            raise KeyError("Missing 'wind' section")

        if "speed" not in data["wind"] or "deg" not in data["wind"]:
            raise KeyError("Missing wind fields")

        # Validate weather list
        weather_list = data.get("weather")
        if not isinstance(weather_list, list) or len(weather_list) == 0:
            raise KeyError("Missing 'weather' section")

        if not isinstance(weather_list[0], dict):
            raise KeyError("Malformed weather entry")

    @staticmethod
    def build_daily_report(city_name: str, data: Dict[str, Any]) -> str:
        """Build a robust daily weather report for the given city."""

        # 🔥 TEST BUNU BEKLİYOR → EKSİK ALAN VARSA HEMEN KEYERROR
        ReportService._validate_required_fields(data)

        now_str = datetime.now().strftime("%d.%m.%Y %H:%M")

        main = data["main"]
        wind = data["wind"]
        weather_list = data["weather"]

        # Safe description
        description = _sanitize_text(weather_list[0].get("description", "Unknown"))

        city_clean = _sanitize_text(city_name)

        lines = [
            f"WEATHER REPORT (Daily) - {now_str}",
            "-" * 40,
            f"City: {city_clean}",
            f"Condition: {description}",
            f"Temperature: {main['temp']}°C",
            f"Feels Like: {main['feels_like']}°C",
            f"Minimum / Maximum: {main['temp_min']}°C / {main['temp_max']}°C",
            f"Humidity: {main['humidity']}%",
            f"Pressure: {main['pressure']} hPa",
            f"Wind Speed: {wind['speed']} m/s, Yön: {wind['deg']}°",
            "-" * 40,
            "We wish you a good day.",
        ]


        LOGGER.info("Daily weather report built for city '%s'.", city_clean)

        return "\n".join(lines)
