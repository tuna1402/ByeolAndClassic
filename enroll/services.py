import logging

from core.services.email import send_enroll_email

logger = logging.getLogger(__name__)


def send_admin_notification(payload: dict) -> None:
    try:
        send_enroll_email(payload)
    except Exception:
        logger.exception("Brevo email failed.")
