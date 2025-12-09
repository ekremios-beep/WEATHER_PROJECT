# tests/test_report_service.py
"""Tests for ReportService (report formatting and data validation)."""

import pytest
from src.services.report_service import ReportService


def test_report_contains_city_name():
    """
    The generated report should include the city name and all essential fields.
    """
    service = ReportService()
    fake_data = {
        "main": {
            "temp": 20,
            "feels_like": 19,
            "temp_min": 18,
            "temp_max": 22,
            "humidity": 60,
            "pressure": 1012,
        },
        "wind": {"speed": 3.5, "deg": 180},
        "weather": [{"description": "partly cloudy"}],
    }

    report = service.build_daily_report("Istanbul", fake_data)

    assert "City: Istanbul" in report
    assert "Temperature: 20°C" in report
    assert "Feels Like:" in report
    assert "Humidity:" in report
    assert "Wind Speed:" in report


def test_report_includes_weather_description():
    """
    The report must include the weather description text.
    """
    service = ReportService()
    fake_data = {
        "main": {
            "temp": 10,
            "feels_like": 8,
            "temp_min": 5,
            "temp_max": 12,
            "humidity": 70,
            "pressure": 1005,
        },
        "wind": {"speed": 2.5, "deg": 200},
        "weather": [{"description": "clear sky"}],
    }

    report = service.build_daily_report("Ankara", fake_data)

    assert "Condition: clear sky" in report


def test_report_missing_weather_key_raises_error():
    """
    If required keys are missing, ReportService should raise a KeyError.
    """
    service = ReportService()
    incomplete_data = {
        "main": {"temp": 20},  # missing 'weather' and other required fields
    }

    with pytest.raises(KeyError):
        service.build_daily_report("Istanbul", incomplete_data)

