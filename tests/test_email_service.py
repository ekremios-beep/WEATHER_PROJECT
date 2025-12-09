# tests/test_email_service.py
"""Tests for EmailService (SMTP mocked)."""

from unittest.mock import patch

from src.services.email_service import EmailService


@patch("smtplib.SMTP")
def test_email_service_sends_email(mock_smtp):
    """EmailService should call SMTP and send a message successfully."""
    service = EmailService()
    service.send_report("test@example.com", "Test Subject", "Body")

    # Ensure SMTP() was called at least once
    assert mock_smtp.called
