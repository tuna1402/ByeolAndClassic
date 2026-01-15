from django.db import models


class SiteBrandSettings(models.Model):
    site_name = models.CharField(max_length=100, default="별앤클래식")
    navbar_logo = models.ImageField(upload_to="brand/", blank=True, null=True)
    main_banner_image = models.ImageField(
        "메인 배너 이미지",
        upload_to="brand/",
        blank=True,
        null=True,
        help_text="홈 상단 메인 배너에 사용되는 이미지입니다.",
    )
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "사이트 브랜딩 설정"
        verbose_name_plural = "사이트 브랜딩 설정"

    def __str__(self) -> str:
        return self.site_name


def get_site_brand_settings() -> "SiteBrandSettings":
    settings, _ = SiteBrandSettings.objects.get_or_create(
        pk=1,
        defaults={"site_name": "별앤클래식"},
    )
    return settings
