import pytest
from django.core.files.uploadedfile import SimpleUploadedFile

from siteconfig.models import HomeBannerSlide


def _make_image(name="banner.gif"):
    return SimpleUploadedFile(
        name=name,
        content=(
            b"GIF89a\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00"
            b"\xff\xff\xff!\xf9\x04\x01\x00\x00\x00\x00,"
            b"\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00;"
        ),
        content_type="image/gif",
    )


@pytest.mark.django_db
def test_home_ok_without_banner_slides(client, settings, tmp_path):
    settings.MEDIA_ROOT = tmp_path
    response = client.get("/")
    assert response.status_code == 200


@pytest.mark.django_db
def test_home_ok_with_banner_slides(client, settings, tmp_path):
    settings.MEDIA_ROOT = tmp_path
    HomeBannerSlide.objects.create(image=_make_image("banner-1.gif"), sort_order=1)
    HomeBannerSlide.objects.create(image=_make_image("banner-2.gif"), sort_order=2)
    response = client.get("/")
    assert response.status_code == 200
