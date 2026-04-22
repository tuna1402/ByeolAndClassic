import pytest
from django.urls import reverse

pytestmark = pytest.mark.django_db


def test_home_ok(client):
    response = client.get(reverse("home"))

    assert response.status_code == 200
