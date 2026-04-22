from django.contrib import admin, messages
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe

from .models import (
    AwardCertificate,
    HomeBannerSlide,
    HomeExamExpertImage,
    HomeFooterHero,
    HomeHeroVideo,
    RoadmapImageCard,
)


@admin.register(HomeBannerSlide)
class HomeBannerSlideAdmin(admin.ModelAdmin):
    list_display = ("thumbnail_preview", "title", "is_active", "sort_order", "created_at")
    list_editable = ("is_active", "sort_order")
    list_filter = ("is_active",)
    ordering = ("sort_order",)
    search_fields = ("title",)
    fields = ("image", "title", "is_active", "sort_order", "thumbnail_preview")
    readonly_fields = ("thumbnail_preview",)

    def thumbnail_preview(self, obj):
        if not obj.image:
            return "미등록"
        return mark_safe(
            f'<img src="{obj.image.url}" alt="{obj.title or "홈 배너"}" style="height: 64px;" />'
        )

    def save_model(self, request, obj, form, change):
        try:
            obj.full_clean()
        except ValidationError as exc:
            self.message_user(request, exc.message_dict.get("image", exc.messages)[0], messages.ERROR)
            return
        super().save_model(request, obj, form, change)

    thumbnail_preview.short_description = "이미지 미리보기"


@admin.register(HomeHeroVideo)
class HomeHeroVideoAdmin(admin.ModelAdmin):
    list_display = ("video_preview", "title", "is_active", "updated_at")
    list_editable = ("is_active",)
    list_filter = ("is_active",)
    ordering = ("-updated_at",)
    fields = ("video", "title", "is_active", "video_preview")
    readonly_fields = ("video_preview",)

    def video_preview(self, obj):
        if not obj or not obj.video:
            return "미등록"
        return mark_safe(
            f'<video src="{obj.video.url}" style="height: 80px;" controls muted playsinline></video>'
        )

    video_preview.short_description = "영상 미리보기"


@admin.register(RoadmapImageCard)
class RoadmapImageCardAdmin(admin.ModelAdmin):
    list_display = ("thumbnail_preview", "is_active", "sort_order", "created_at")
    list_editable = ("is_active", "sort_order")
    ordering = ("sort_order",)
    fields = ("image", "is_active", "sort_order", "thumbnail_preview")
    readonly_fields = ("thumbnail_preview",)

    def thumbnail_preview(self, obj):
        if not obj.image:
            return "미등록"
        return mark_safe(
            f'<img src="{obj.image.url}" alt="로드맵 이미지" style="height: 64px;" />'
        )

    thumbnail_preview.short_description = "이미지 미리보기"


@admin.register(AwardCertificate)
class AwardCertificateAdmin(admin.ModelAdmin):
    list_display = ("thumbnail_preview", "title", "year", "is_active", "sort_order")
    list_editable = ("is_active", "sort_order")
    ordering = ("sort_order",)
    fields = ("title", "year", "image", "is_active", "sort_order", "thumbnail_preview")
    readonly_fields = ("thumbnail_preview",)

    def thumbnail_preview(self, obj):
        if not obj.image:
            return "미등록"
        alt_text = obj.title or "수상 경력"
        return mark_safe(
            f'<img src="{obj.image.url}" alt="{alt_text}" style="height: 64px;" />'
        )

    thumbnail_preview.short_description = "이미지 미리보기"


@admin.register(HomeExamExpertImage)
class HomeExamExpertImageAdmin(admin.ModelAdmin):
    list_display = ("thumbnail_preview", "alt_text", "is_active", "sort_order")
    list_editable = ("is_active", "sort_order")
    ordering = ("sort_order",)
    fields = ("image", "alt_text", "is_active", "sort_order", "thumbnail_preview")
    readonly_fields = ("thumbnail_preview",)

    def thumbnail_preview(self, obj):
        if not obj or not obj.image:
            return "미등록"
        alt_text = obj.alt_text or "입시 전문가 이미지"
        return mark_safe(
            f'<img src="{obj.image.url}" alt="{alt_text}" style="height: 64px; border-radius: 8px;" />'
        )

    def save_model(self, request, obj, form, change):
        try:
            obj.full_clean()
        except ValidationError as exc:
            self.message_user(request, exc.message_dict.get("image", exc.messages)[0], messages.ERROR)
            return
        super().save_model(request, obj, form, change)

    thumbnail_preview.short_description = "이미지 미리보기"


@admin.register(HomeFooterHero)
class HomeFooterHeroAdmin(admin.ModelAdmin):
    list_display = ("thumbnail_preview", "title", "is_active", "updated_at")
    list_editable = ("is_active",)
    ordering = ("-updated_at",)
    fields = (
        "image",
        "title",
        "subtitle",
        "cta_label",
        "cta_url",
        "is_active",
        "thumbnail_preview",
    )
    readonly_fields = ("thumbnail_preview",)

    def thumbnail_preview(self, obj):
        if not obj or not obj.image:
            return "미등록"
        return mark_safe(
            f'<img src="{obj.image.url}" alt="{obj.title}" style="height: 80px; border-radius: 8px;" />'
        )

    thumbnail_preview.short_description = "이미지 미리보기"
