import pytest
from django.template.loader import render_to_string
from django.urls import reverse

from siteconfig.models import SiteBrandSettings

pytestmark = pytest.mark.django_db


def test_home_ok_without_site_brand_settings(client):
    SiteBrandSettings.objects.all().delete()

    response = client.get(reverse("home"))

    assert response.status_code == 200


def test_home_ok_with_site_brand_settings(client):
    SiteBrandSettings.objects.create(site_name="테스트")

    response = client.get(reverse("home"))

    assert response.status_code == 200


def test_home_template_uses_main_banner_image_field():
    site_brand = SiteBrandSettings(site_name="테스트")

    rendered = render_to_string("pages/home.html", {"site_brand": site_brand})

    assert "main-visual" in rendered
