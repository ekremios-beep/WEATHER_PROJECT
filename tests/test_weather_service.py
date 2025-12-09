# tests/test_weather_service.py
"""Tests for WeatherService (requests mocked)."""

from unittest.mock import patch, MagicMock
import pytest

from src.services.weather_service import WeatherService
from src.utils.exceptions import WeatherApiError


def test_weather_service_successful_response():
    """WeatherService should return parsed JSON when API responds normally."""
    service = WeatherService()

    fake_response = {
        "main": {
            "temp": 20,
            "feels_like": 18,
            "temp_min": 15,
            "temp_max": 22,
            "humidity": 55,
            "pressure": 1015,
        },
        "wind": {"speed": 3.0, "deg": 180},
        "weather": [{"description": "açık hava"}],
    }

    mock_resp = MagicMock()
    mock_resp.ok = True
    mock_resp.json.return_value = fake_response

    with patch("requests.get", return_value=mock_resp):
        data = service.get_current_weather("Istanbul")
        assert data["main"]["temp"] == 20
        assert data["weather"][0]["description"] == "açık hava"


def test_weather_service_invalid_json():
    """WeatherService should raise WeatherApiError when JSON decoding fails."""
    service = WeatherService()

    mock_resp = MagicMock()
    mock_resp.ok = True
    mock_resp.json.side_effect = ValueError("Bad JSON")

    with patch("requests.get", return_value=mock_resp):
        with pytest.raises(WeatherApiError):
            service.get_current_weather("Ankara")


def test_weather_service_http_error():
    """WeatherService should raise WeatherApiError on non-200 HTTP responses."""
    service = WeatherService()

    mock_resp = MagicMock()
    mock_resp.ok = False
    mock_resp.status_code = 500
    mock_resp.text = "Internal Server Error"

    with patch("requests.get", return_value=mock_resp):
        with pytest.raises(WeatherApiError):
            service.get_current_weather("Izmir")


def test_weather_service_retries_then_fails():
    """WeatherService should retry and then raise WeatherApiError after failures."""
    service = WeatherService(max_retries=2, retry_delay=0)  # speed up tests

    # Always fail (simulate timeout or network error)
    with patch("requests.get", side_effect=Exception("Network Down")):
        with pytest.raises(WeatherApiError):
            service.get_current_weather("Bursa")
