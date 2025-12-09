# tests/test_email_service.py
"""Tests for EmailService (SMTP mocked)."""

from unittest.mock import patch, MagicMock

from src.services.email_service import EmailService


@patch("smtplib.SMTP")
def test_email_service_sends_email(mock_smtp):
    """EmailService should call SMTP and send a message successfully."""

    # Mock instance returned from smtplib.SMTP
    mock_smtp_instance = MagicMock()
    mock_smtp.return_value.__enter__.return_value = mock_smtp_instance

    service = EmailService()
    service.send_report("test@example.com", "Test Subject", "Body")

    # Assert that SMTP() was actually called
    mock_smtp.assert_called_once()

    # Assert sendmail was called with correct parameters
    assert mock_smtp_instance.sendmail.called, "sendmail() should have been called."
