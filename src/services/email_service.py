# src/services/email_service.py
"""Service responsible for sending emails with weather reports."""

from __future__ import annotations

import re
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from ..config import get_settings
from ..utils.exceptions import EmailSendError
from ..utils.logger import get_logger


LOGGER = get_logger()

# Stronger RFC 5322–inspired email pattern
EMAIL_REGEX = re.compile(
    r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
)


class EmailService:
    """SMTP email sender for weather reports."""

    def __init__(self) -> None:
        self._settings = get_settings()

    @staticmethod
    def _validate_email(address: str) -> None:
        """Validate email format and prevent header injection."""
        if "\n" in address or "\r" in address:
            raise EmailSendError("Invalid email address (newline not allowed).")

        if not EMAIL_REGEX.match(address):
            raise EmailSendError("Invalid email address format.")

    @staticmethod
    def _sanitize_header(value: str) -> str:
        """Strip newline characters from header fields."""
        if not isinstance(value, str):
            return ""
        return value.replace("\n", " ").replace("\r", " ").strip()

    @staticmethod
    def _sanitize_body(text: str) -> str:
        """Optional body sanitation to avoid formatting issues."""
        if not isinstance(text, str):
            return ""
        return text.replace("\r", "").strip()

    def _build_message(self, to_email: str, subject: str, body: str) -> MIMEMultipart:
        """Construct the MIME email object."""
        msg = MIMEMultipart()
        msg["From"] = self._sanitize_header(self._settings.from_email)
        msg["To"] = self._sanitize_header(to_email)
        msg["Subject"] = self._sanitize_header(subject)

        msg.attach(MIMEText(self._sanitize_body(body), "plain", "utf-8"))
        return msg

    def send_report(self, to_email: str, subject: str, body: str) -> None:
        """Send a plain-text email with improved safety and logging."""
        self._validate_email(to_email)
        msg = self._build_message(to_email, subject, body)

        try:
            with smtplib.SMTP(
                self._settings.smtp_host,
                self._settings.smtp_port,
                timeout=15,
            ) as server:
                server.ehlo()

                # TLS protection
                try:
                    server.starttls()
                    server.ehlo()
                except smtplib.SMTPException as exc:
                    LOGGER.error("TLS negotiation failed: %s", exc)
                    raise EmailSendError("TLS negotiation failed.") from exc

                # Login
                try:
                    server.login(self._settings.smtp_user, self._settings.smtp_password)
                except smtplib.SMTPAuthenticationError as exc:
                    LOGGER.error("SMTP authentication failed: %s", exc)
                    raise EmailSendError("Invalid SMTP credentials.") from exc

                try:
                    server.sendmail(
                        self._settings.from_email,
                        to_email,
                        msg.as_string()
                    )
                except Exception as exc:
                    LOGGER.error("sendmail() failed: %s", exc)
                    raise EmailSendError("Failed to send email.") from exc

        except (smtplib.SMTPConnectError, smtplib.SMTPServerDisconnected) as exc:
            LOGGER.error("SMTP connection error: %s", exc)
            raise EmailSendError("SMTP connection error.") from exc

        except smtplib.SMTPException as exc:
            LOGGER.error("General SMTP error: %s", exc)
            raise EmailSendError("An SMTP error occurred.") from exc

        except OSError as exc:
            LOGGER.error("Network I/O error while sending email: %s", exc)
            raise EmailSendError("Network error occurred during email sending.") from exc

        LOGGER.info("Report email successfully sent to %s", to_email)
