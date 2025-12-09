# src/services/city_service.py
"""Service responsible for managing city list and user selection."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

from ..config import get_settings
from ..utils.logger import get_logger


LOGGER = get_logger()


@dataclass(frozen=True)
class City:
    """Represents a city entry."""

    id: int
    name: str
    query: str


class CityService:
    """Service class for loading and selecting Turkish cities."""

    def __init__(self) -> None:
        self._settings = get_settings()
        self._cities: List[City] = []
        self._load_cities()

    @property
    def cities(self) -> List[City]:
        """Return list of available cities."""
        return self._cities

    def _load_cities(self) -> None:
        """Load cities from JSON file or use fallback list."""
        if self._settings.cities_file_path:
            path = Path(self._settings.cities_file_path)
        else:
            path = Path("data") / "turkey_cities.json"

        try:
            with path.open("r", encoding="utf-8") as file:
                data = json.load(file)
            self._cities = [
                City(id=item["id"], name=item["name"], query=item["query"])
                for item in data
            ]
            LOGGER.info("Loaded %d cities from %s", len(self._cities), path)
        except FileNotFoundError:
            LOGGER.error("City file not found at %s", path)
            raise
        except (KeyError, TypeError, json.JSONDecodeError) as exc:
            LOGGER.error("Failed to parse city file %s: %s", path, exc)
            raise

    def get_city_by_id(self, city_id: int) -> Optional[City]:
        """Return a city by its ID, or None if not found."""
        return next((c for c in self._cities if c.id == city_id), None)

    # Kullanıcı etkileşimli seçim
    def prompt_user_for_city(self) -> City:
        """Interactively ask user to select a city from the list.

        This method is robust against invalid inputs and will loop
        until a valid city ID is provided or the user cancels.
        """
        print("=== Türkiye İlleri Hava Raporu ===")
        for city in self._cities:
            print(f"{city.id:2d} - {city.name}")

        while True:
            try:
                raw = input(
                    "Please enter the city ID (or 'q' to quit): ",
                ).strip()
            except (EOFError, KeyboardInterrupt) as exc:
                print("\nInput cancelled by user.")
                LOGGER.warning("User cancelled input while selecting city.")
                raise SystemExit(1) from exc


            if raw.lower() in {"q", "quit", "exit"}:
                print("Exiting application.")
                LOGGER.info("User chose to exit during city selection.")
                raise SystemExit(0)

            if not raw.isdigit():
                print("Please enter a valid numeric city ID.")
                continue

            city_id = int(raw)
            if city_id <= 0:
                print("City ID must be a positive integer.")
                continue

            city = self.get_city_by_id(city_id)
            if city is None:
                print("No city found for this ID. Please try again.")
            else:
                LOGGER.info("User selected city: %s (%s)", city.name, city.query)
                return city
