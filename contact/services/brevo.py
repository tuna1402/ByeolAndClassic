import logging

import requests
from django.conf import settings

from contact.models import ContactMessage

logger = logging.getLogger(__name__)


def _build_headers() -> dict:
    api_key = getattr(settings, "BREVO_API_KEY", "")
    if not api_key:
        raise ValueError("BREVO_API_KEY is missing.")
    return {
        "api-key": api_key,
        "accept": "application/json",
        "content-type": "application/json",
    }


def send_contact_email(contact_message: ContactMessage) -> None:
    sender_email = getattr(settings, "CONTACT_FROM_EMAIL", "")
    recipient_email = getattr(settings, "CONTACT_TO_EMAIL", "")

    if not sender_email or not recipient_email:
        raise ValueError("CONTACT_FROM_EMAIL or CONTACT_TO_EMAIL is missing.")

    body = {
        "sender": {"name": "ByeolAndClassic", "email": sender_email},
        "to": [{"email": recipient_email}],
        "subject": "[별앤클래식] 문의가 접수되었습니다",
        "textContent": (
            "새로운 문의가 접수되었습니다.\n"
            f"이름: {contact_message.name}\n"
            f"연락처: {contact_message.phone}\n"
            f"이메일: {contact_message.email or '-'}\n"
            f"문의 내용: {contact_message.message}\n"
        ),
    }
    response = requests.post(
        "https://api.brevo.com/v3/smtp/email",
        json=body,
        headers=_build_headers(),
        timeout=10,
    )
    response.raise_for_status()
    logger.info("Brevo email status: %s", response.status_code)
