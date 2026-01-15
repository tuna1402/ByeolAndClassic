import pytest
from django.urls import reverse

from siteconfig.models import SiteBrandSettings

pytestmark = pytest.mark.django_db


def test_site_brand_context_processor(client):
    SiteBrandSettings.objects.create(site_name="테스트")

    response = client.get(reverse("home"))

    assert response.context["site_brand"].site_name == "테스트"
