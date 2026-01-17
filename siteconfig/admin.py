from django.contrib import admin, messages
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.safestring import mark_safe

from .models import (
    AwardCertificate,
    HomeBannerSlide,
    RoadmapImageCard,
    SiteBrandSettings,
    get_site_brand_settings,
)


@admin.register(SiteBrandSettings)
class SiteBrandSettingsAdmin(admin.ModelAdmin):
    list_display = ("site_name", "updated_at")
    readonly_fields = (
        "created_at",
        "updated_at",
        "navbar_logo_preview",
        "main_banner_preview",
    )
    fieldsets = (
        ("기본", {"fields": ("site_name",)}),
        ("Navbar-brand", {"fields": ("navbar_logo", "navbar_logo_preview")}),
        ("메인 배너", {"fields": ("main_banner_image", "main_banner_preview")}),
        ("타임스탬프", {"fields": ("created_at", "updated_at")}),
    )

    def has_add_permission(self, request):
        return False

    def changelist_view(self, request, extra_context=None):
        settings_obj = get_site_brand_settings()
        url = reverse("admin:siteconfig_sitebrandsettings_change", args=(settings_obj.pk,))
        return HttpResponseRedirect(url)

    def navbar_logo_preview(self, obj):
        if not obj.navbar_logo:
            return "미등록"
        return mark_safe(
            f'<img src="{obj.navbar_logo.url}" alt="{obj.site_name}" style="height: 48px;" />'
        )

    def main_banner_preview(self, obj):
        if not obj.main_banner_image:
            return "미등록"
        return mark_safe(
            """
            <div>
              <img src="{url}" alt="{name}" style="max-height: 120px; max-width: 100%;" />
            </div>
            """.format(url=obj.main_banner_image.url, name=obj.site_name)
        )

    navbar_logo_preview.short_description = "Navbar 로고 미리보기"
    main_banner_preview.short_description = "메인 배너 이미지 미리보기"


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
    list_display = ("thumbnail_preview", "title", "is_active", "sort_order")
    list_editable = ("is_active", "sort_order")
    ordering = ("sort_order",)
    fields = ("title", "image", "is_active", "sort_order", "thumbnail_preview")
    readonly_fields = ("thumbnail_preview",)

    def thumbnail_preview(self, obj):
        if not obj.image:
            return "미등록"
        alt_text = obj.title or "수상 경력"
        return mark_safe(
            f'<img src="{obj.image.url}" alt="{alt_text}" style="height: 64px;" />'
        )

    thumbnail_preview.short_description = "이미지 미리보기"
