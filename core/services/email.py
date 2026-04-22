import logging
from django.conf import settings

logger = logging.getLogger(__name__)


def _build_common_headers() -> dict:
    api_key = getattr(settings, "BREVO_API_KEY", "")
    if not api_key:
        raise ValueError("BREVO_API_KEY is missing.")
    return {
        "api-key": api_key,
        "accept": "application/json",
        "content-type": "application/json",
    }


def _send_email(payload: dict) -> None:
    import requests

    response = requests.post(
        "https://api.brevo.com/v3/smtp/email",
        json=payload,
        headers=_build_common_headers(),
        timeout=10,
    )
    response.raise_for_status()
    logger.info("Brevo email status: %s", response.status_code)


def send_contact_email(payload: dict) -> None:
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
            f"이름: {payload['name']}\n"
            f"연락처: {payload['phone']}\n"
            f"이메일: {payload.get('email') or '-'}\n"
            f"문의 내용: {payload['message']}\n"
        ),
    }
    _send_email(body)


def send_enroll_email(payload: dict) -> None:
    sender_email = getattr(settings, "BREVO_SENDER_EMAIL", "") or getattr(
        settings, "CONTACT_FROM_EMAIL", ""
    )
    sender_name = getattr(settings, "BREVO_SENDER_NAME", "ByeolAndClassic")
    recipient_email = getattr(settings, "BREVO_ADMIN_EMAIL", "") or getattr(
        settings, "CONTACT_TO_EMAIL", ""
    )

    if not sender_email or not recipient_email:
        raise ValueError(
            "Missing sender/recipient for enroll mail. "
            "Set BREVO_SENDER_EMAIL/BREVO_ADMIN_EMAIL or CONTACT_FROM_EMAIL/CONTACT_TO_EMAIL."
        )

    body = {
        "sender": {"name": sender_name, "email": sender_email},
        "to": [{"email": recipient_email}],
        "subject": "[별앤클래식] 수강신청이 접수되었습니다",
        "textContent": (
            "새로운 수강신청이 접수되었습니다.\n"
            f"이름: {payload['name']}\n"
            f"연락처: {payload['phone']}\n"
            f"생년월일: {payload['birth_date']}\n"
            f"거주지: {payload['residence']}\n"
            f"상담 유형: {', '.join(payload['consultation_types'])}\n"
            f"레벨테스트 연주곡: {payload['level_test_piece']}\n"
            f"희망 학교: {payload['career_school']}\n"
            f"수상내역: {payload['awards_history']}\n"
            f"피아노 연습량: {payload['practice_time']}\n"
            f"학교 성적: {payload['school_grade']}\n"
            f"성적표 지참 가능 여부: {'가능' if payload['transcript_available'] else '불가'}\n"
            f"희망일: {payload['preferred_date']}\n"
            f"문의 내용: {payload['message']}\n"
        ),
    }
    _send_email(body)
