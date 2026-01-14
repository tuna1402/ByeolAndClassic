import pytest
from django.urls import reverse

from contact.models import ContactMessage


@pytest.mark.django_db
def test_contact_form_get(client):
    response = client.get(reverse("contact_form"))
    assert response.status_code == 200
    assert "문의하기" in response.content.decode("utf-8")


@pytest.mark.django_db
def test_contact_form_post_creates_message(client, monkeypatch):
    monkeypatch.setattr("contact.views.send_contact_email", lambda payload: None)

    response = client.post(
        reverse("contact_form"),
        data={
            "name": "테스트",
            "phone": "010-1111-2222",
            "email": "test@example.com",
            "message": "문의합니다.",
        },
    )

    assert response.status_code == 302
    assert response.url == reverse("contact_done")
    assert ContactMessage.objects.count() == 1
