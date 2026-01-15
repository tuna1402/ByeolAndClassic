import pytest
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile

from siteconfig.models import HomeBannerSlide, MAX_HOME_BANNER_SLIDES


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
def test_home_banner_slide_limit(settings, tmp_path):
    settings.MEDIA_ROOT = tmp_path
    for idx in range(MAX_HOME_BANNER_SLIDES):
        slide = HomeBannerSlide(image=_make_image(f"banner-{idx}.gif"), sort_order=idx + 1)
        slide.full_clean()
        slide.save()

    extra_slide = HomeBannerSlide(image=_make_image("banner-extra.gif"), sort_order=10)
    with pytest.raises(ValidationError):
        extra_slide.full_clean()
