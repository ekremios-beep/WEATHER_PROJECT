# src/app.py
"""
Application entrypoint for the Turkey Weather Reporter.

Handles city selection, user input validation, weather API integration,
database persistence and email report delivery with full error handling.
"""


from __future__ import annotations

from .services.city_service import CityService
from .services.database_service import DatabaseService
from .services.email_service import EmailService
from .services.report_service import ReportService
from .services.weather_service import WeatherService
from .utils.exceptions import DatabaseError, EmailSendError, WeatherApiError
from .utils.logger import get_logger


LOGGER = get_logger()


def _prompt_email() -> str:
    """Ask user for a valid email and sanitize input against injection attacks."""
    while True:
        try:
            raw = input("Please enter the email address to send the report to: ").strip()
        except EOFError:
            print("[ERROR] Unexpected input termination. Please try again.")
            continue

        # Basic validation
        if raw == "":
            print("[ERROR] Email cannot be empty.")
            continue

        # Prevent header injection
        if "\n" in raw or "\r" in raw:
            print("[ERROR] Invalid email format.")
            continue

        # Basic structural check
        if "@" not in raw or "." not in raw:
            print("[ERROR] Invalid email address format.")
            continue

        return raw


def main() -> None:
    """
    Application core logic (may raise custom exceptions).
    This is intentionally not wrapped in try/except for clean separation.
    """
    city_service = CityService()
    weather_service = WeatherService()
    db_service = DatabaseService()
    report_service = ReportService()
    email_service = EmailService()

    # 1) Ask user to choose a city safely
    city = city_service.prompt_user_for_city()

    # 2) Ask and validate email address
    to_email = _prompt_email()

    # 3) Fetch weather
    weather_data = weather_service.get_current_weather(city.query)

    # 4) Save to database
    db_service.save_weather_report(city.name, weather_data)

    # 5) Build formatted report
    report_text = report_service.build_daily_report(city.name, weather_data)

    # 6) Send email
    subject = f"{city.name} Daily Weather Report"
    email_service.send_report(to_email, subject, report_text)

    print("\nReport successfully generated and sent via email.")
    LOGGER.info("Weather report process completed successfully.")


def run() -> None:
    """Safe entrypoint: handles all top-level exceptions."""
    try:
        main()
    except WeatherApiError as exc:
        print(f"[ERROR] Could not fetch weather data: {exc}")
        LOGGER.error("WeatherApiError: %s", exc)
    except DatabaseError as exc:
        print(f"[ERROR] Could not save data to database: {exc}")
        LOGGER.error("DatabaseError: %s", exc)
    except EmailSendError as exc:
        print(f"[ERROR] Could not send email: {exc}")
        LOGGER.error("EmailSendError: %s", exc)
    except SystemExit as exc:
        LOGGER.info("User exited: %s", exc)
    except Exception as exc:  # pylint:disable=broad-except
        print("[ERROR] An unexpected error occurred. See logs for details.")
        LOGGER.exception("Unhandled exception: %s", exc)


if __name__ == "__main__":
    run()
