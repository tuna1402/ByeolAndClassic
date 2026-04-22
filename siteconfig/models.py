from django.core.exceptions import ValidationError
from django.db import models

MAX_HOME_BANNER_SLIDES = 5
MAX_HOME_EXAM_EXPERT_IMAGES = 3


class HomeHeroVideo(models.Model):
    video = models.FileField(
        upload_to="brand/home-hero/",
        help_text="홈 히어로 mp4 영상 (권장 1920x780)",
    )
    title = models.CharField(max_length=120, blank=True)
    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-updated_at", "-created_at"]
        verbose_name = "홈 히어로 영상"
        verbose_name_plural = "홈 히어로 영상"

    def __str__(self) -> str:
        return self.title or f"홈 히어로 영상 #{self.pk or '신규'}"


class HomeBannerSlide(models.Model):
    image = models.ImageField(
        upload_to="brand/banners/",
        help_text="홈 상단 슬라이드 이미지. 권장: 1600x900",
    )
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
    image = models.ImageField(
        upload_to="brand/roadmap/",
        help_text="로드맵 이미지 카드. 권장: 900x600",
    )
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
    year = models.CharField(max_length=4, blank=True)
    image = models.ImageField(
        upload_to="brand/awards/",
        help_text="수상 경력 이미지. 권장: 900x1200",
    )
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


class HomeExamExpertImage(models.Model):
    image = models.ImageField(
        upload_to="brand/home-exam-expert/",
        help_text="홈 입시 전문가 섹션 이미지. 권장: 900x1200",
    )
    alt_text = models.CharField(max_length=120, blank=True)
    is_active = models.BooleanField(default=True)
    sort_order = models.PositiveSmallIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["sort_order", "-created_at"]
        verbose_name = "홈 입시 전문가 이미지"
        verbose_name_plural = "홈 입시 전문가 이미지"

    def __str__(self) -> str:
        return self.alt_text or f"홈 입시 전문가 이미지 #{self.pk or '신규'}"

    def clean(self) -> None:
        super().clean()
        existing_count = HomeExamExpertImage.objects.exclude(pk=self.pk).count()
        if existing_count >= MAX_HOME_EXAM_EXPERT_IMAGES:
            raise ValidationError(
                {"image": "홈 입시 전문가 이미지는 최대 3장까지 등록할 수 있습니다."}
            )


class HomeFooterHero(models.Model):
    image = models.ImageField(
        upload_to="brand/home-footer/",
        blank=True,
        null=True,
        help_text="푸터 위 히어로 배경 이미지",
    )
    title = models.CharField(max_length=120, default="상담으로 시작하는 입시 준비")
    subtitle = models.CharField(
        max_length=220,
        default="맞춤형 커리큘럼 상담으로 목표 학교 합격 로드맵을 설계해보세요.",
    )
    cta_label = models.CharField(max_length=50, default="상담 신청하기")
    cta_url = models.CharField(max_length=200, default="/enroll/")
    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-updated_at", "-created_at"]
        verbose_name = "홈 푸터 히어로"
        verbose_name_plural = "홈 푸터 히어로"

    def __str__(self) -> str:
        return self.title or f"홈 푸터 히어로 #{self.pk or '신규'}"
