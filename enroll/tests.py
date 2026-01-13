import pytest
from django.urls import reverse

from enroll.models import EnrollApplication


@pytest.mark.django_db
def test_enroll_form_get(client):
    response = client.get(reverse("enroll_form"))
    assert response.status_code == 200
    assert "수강신청" in response.content.decode("utf-8")


@pytest.mark.django_db
def test_enroll_form_post_creates_application(client, monkeypatch):
    monkeypatch.setattr("enroll.views.send_admin_notification", lambda payload: None)

    response = client.post(
        reverse("enroll_form"),
        data={
            "name": "테스트",
            "phone": "010-0000-0000",
            "birth_date": "2000-01-01",
            "residence": "서울",
            "purposes": ["예술중", "음대입시"],
            "preferred_date": "2024-12-31",
            "message": "문의합니다.",
        },
    )

    assert response.status_code == 200
    assert EnrollApplication.objects.count() == 1
    application = EnrollApplication.objects.get()
    assert application.name == "테스트"
    assert application.purposes == ["예술중", "음대입시"]
