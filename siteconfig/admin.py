from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.safestring import mark_safe

from .models import SiteBrandSettings, get_site_brand_settings


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
