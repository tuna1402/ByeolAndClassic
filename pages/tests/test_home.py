import pytest
from django.urls import reverse

pytestmark = pytest.mark.django_db

def test_home_ok(client):
    url = reverse("home")
    res = client.get(url)
    assert res.status_code == 200
