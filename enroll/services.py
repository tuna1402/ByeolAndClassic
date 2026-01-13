import json
import logging
from urllib import request

from django.conf import settings

logger = logging.getLogger(__name__)


def send_admin_notification(payload: dict) -> None:
    api_key = getattr(settings, "BREVO_API_KEY", "")
    sender_email = getattr(settings, "BREVO_SENDER_EMAIL", "")
    sender_name = getattr(settings, "BREVO_SENDER_NAME", "ByeolAndClassic")
    admin_email = getattr(settings, "BREVO_ADMIN_EMAIL", "")

    if not api_key or not sender_email or not admin_email:
        logger.info("Brevo email skipped: missing configuration.")
        return

    body = {
        "sender": {"name": sender_name, "email": sender_email},
        "to": [{"email": admin_email}],
        "subject": "[별앤클래식] 수강신청이 접수되었습니다",
        "textContent": (
            "새로운 수강신청이 접수되었습니다.\n"
            f"이름: {payload['name']}\n"
            f"연락처: {payload['phone']}\n"
            f"생년월일: {payload['birth_date']}\n"
            f"거주지: {payload['residence']}\n"
            f"수강 목적: {', '.join(payload['purposes'])}\n"
            f"희망일: {payload['preferred_date']}\n"
            f"문의 내용: {payload['message']}\n"
        ),
    }

    data = json.dumps(body).encode("utf-8")
    req = request.Request(
        "https://api.brevo.com/v3/smtp/email",
        data=data,
        headers={
            "api-key": api_key,
            "accept": "application/json",
            "content-type": "application/json",
        },
        method="POST",
    )

    try:
        with request.urlopen(req, timeout=10) as response:
            logger.info("Brevo email status: %s", response.status)
    except Exception:
        logger.exception("Brevo email failed.")
