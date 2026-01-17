import io

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from PIL import Image

from siteconfig.models import AwardCertificate, RoadmapImageCard

pytestmark = pytest.mark.django_db


def _make_test_image(name="test.jpg"):
    buffer = io.BytesIO()
    image = Image.new("RGB", (40, 40), color=(120, 120, 120))
    image.save(buffer, format="JPEG")
    buffer.seek(0)
    return SimpleUploadedFile(name, buffer.read(), content_type="image/jpeg")


def test_home_ok_without_roadmap_images(client):
    RoadmapImageCard.objects.all().delete()

    response = client.get(reverse("home"))

    assert response.status_code == 200


def test_home_ok_without_awards(client):
    AwardCertificate.objects.all().delete()

    response = client.get(reverse("home"))

    assert response.status_code == 200


def test_home_ok_with_roadmap_and_awards(client):
    image_file = _make_test_image()
    RoadmapImageCard.objects.create(image=image_file)
    AwardCertificate.objects.create(image=_make_test_image(name="award.jpg"), title="테스트")

    response = client.get(reverse("home"))

    assert response.status_code == 200
