# tests/test_report_service.py
"""Tests for ReportService."""

from src.services.report_service import ReportService


def test_report_contains_city_name():
    """Report should include the city name and basic weather fields."""
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
        "weather": [{"description": "parçalı bulutlu"}],
    }

    report = service.build_daily_report("İstanbul", fake_data)

    assert "İl: İstanbul" in report
    assert "Sıcaklık:" in report
