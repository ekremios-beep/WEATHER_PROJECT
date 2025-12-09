# tests/test_city_service.py
"""Unit tests for CityService."""

import json
import pytest

from src.services.city_service import CityService


def create_temp_city_file(tmp_path):
    """Create a temporary JSON file for testing."""
    data = [
        {"id": 1, "name": "Istanbul", "query": "Istanbul"},
        {"id": 2, "name": "Ankara", "query": "Ankara"},
    ]
    file_path = tmp_path / "cities.json"
    file_path.write_text(json.dumps(data), encoding="utf-8")
    return file_path


def test_city_service_loads_custom_file(tmp_path, monkeypatch):
    """CityService should load cities from a given JSON path."""
    city_file = create_temp_city_file(tmp_path)

    # patch environment variable
    monkeypatch.setenv("CITIES_FILE_PATH", str(city_file))

    service = CityService()

    assert len(service.cities) == 2
    names = {city.name for city in service.cities}
    assert "Istanbul" in names
    assert "Ankara" in names


def test_city_service_get_city_by_id(tmp_path, monkeypatch):
    """get_city_by_id() should return the correct city instance."""
    city_file = create_temp_city_file(tmp_path)
    monkeypatch.setenv("CITIES_FILE_PATH", str(city_file))

    service = CityService()
    city = service.get_city_by_id(1)

    assert city is not None
    assert city.name == "Istanbul"


def test_city_service_invalid_json(tmp_path, monkeypatch):
    """CityService should raise an error if JSON file is invalid."""
    bad_file = tmp_path / "broken.json"
    bad_file.write_text("{invalid-json}", encoding="utf-8")

    monkeypatch.setenv("CITIES_FILE_PATH", str(bad_file))

    with pytest.raises(Exception):
        CityService()


def test_city_service_missing_file(tmp_path, monkeypatch):
    """Missing file should raise FileNotFoundError."""
    missing_path = tmp_path / "no_file.json"
    monkeypatch.setenv("CITIES_FILE_PATH", str(missing_path))

    with pytest.raises(FileNotFoundError):
        CityService()
