import logging
from typing import Optional
from app.config.settings import settings

logger = logging.getLogger("datapilot.email")

class EmailService:
    @staticmethod
    def send_email(to_email: str, subject: str, body: str, html_body: Optional[str] = None) -> bool:
        """Send email via configured provider (console logging for development)."""
        logger.info(f"[EMAIL] To: {to_email} | Subject: {subject}")
        logger.info(f"[EMAIL BODY]\n{body}")
        return True

    @staticmethod
    def send_welcome_email(to_email: str, user_name: str) -> bool:
        subject = f"Welcome to {settings.APP_NAME}!"
        body = f"Hello {user_name},\n\nWelcome to {settings.APP_NAME}! You can now start uploading Excel/CSV files and turn your raw data into actionable decisions.\n\nBest,\nThe DataPilot Team"
        return EmailService.send_email(to_email, subject, body)

    @staticmethod
    def send_report_ready_email(to_email: str, report_title: str, report_url: str) -> bool:
        subject = f"Your Report '{report_title}' is Ready"
        body = f"Your executive PDF report '{report_title}' has been generated and is ready for download:\n{report_url}\n\nDataPilot AI"
        return EmailService.send_email(to_email, subject, body)

    @staticmethod
    def send_password_reset_email(to_email: str, reset_token: str) -> bool:
        reset_link = f"{settings.FRONTEND_URL}/reset-password?token={reset_token}"
        subject = "Reset Your Password - DataPilot AI"
        body = f"You requested a password reset. Click the link below to set a new password:\n{reset_link}\n\nIf you did not request this, you can safely ignore this email."
        return EmailService.send_email(to_email, subject, body)

