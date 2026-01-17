from django.core.exceptions import ValidationError
from django.db import models

MAX_HOME_BANNER_SLIDES = 5


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


class HomeBannerSlide(models.Model):
    image = models.ImageField(upload_to="brand/banners/")
    title = models.CharField(max_length=120, blank=True)
    is_active = models.BooleanField(default=True)
    sort_order = models.PositiveSmallIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["sort_order", "-created_at"]
        verbose_name = "홈 배너 슬라이드"
        verbose_name_plural = "홈 배너(슬라이드)"

    def __str__(self) -> str:
        return self.title or f"홈 배너 슬라이드 #{self.pk or '신규'}"

    def clean(self) -> None:
        super().clean()
        existing_count = HomeBannerSlide.objects.exclude(pk=self.pk).count()
        if existing_count >= MAX_HOME_BANNER_SLIDES:
            raise ValidationError({"image": "홈 배너 슬라이드는 최대 5장까지 등록할 수 있습니다."})


class RoadmapImageCard(models.Model):
    image = models.ImageField(upload_to="brand/roadmap/")
    is_active = models.BooleanField(default=True)
    sort_order = models.PositiveSmallIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["sort_order", "-created_at"]
        verbose_name = "로드맵 이미지 카드"
        verbose_name_plural = "로드맵 이미지 카드"

    def __str__(self) -> str:
        return f"로드맵 이미지 #{self.pk or '신규'}"


class AwardCertificate(models.Model):
    title = models.CharField(max_length=120, blank=True)
    image = models.ImageField(upload_to="brand/awards/")
    is_active = models.BooleanField(default=True)
    sort_order = models.PositiveSmallIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["sort_order", "-created_at"]
        verbose_name = "수상 경력 이미지"
        verbose_name_plural = "수상 경력 이미지"

    def __str__(self) -> str:
        return self.title or f"수상 경력 이미지 #{self.pk or '신규'}"


def get_site_brand_settings() -> "SiteBrandSettings":
    settings, _ = SiteBrandSettings.objects.get_or_create(
        pk=1,
        defaults={"site_name": "별앤클래식"},
    )
    return settings
