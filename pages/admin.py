from django.contrib import admin
from django.utils.html import format_html

from .models import PageContent


@admin.register(PageContent)
class PageContentAdmin(admin.ModelAdmin):
    list_display = ("key", "title", "updated_at")
    search_fields = ("key", "title", "content")
    readonly_fields = ("created_at", "updated_at", "hero_image_preview")

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "key",
                    "title",
                    "content",
                    "hero_image",
                    "hero_image_preview",
                    "attachment",
                )
            },
        ),
        ("Timestamps", {"fields": ("created_at", "updated_at")}),
    )

    @admin.display(description="Hero Preview")
    def hero_image_preview(self, obj):
        if not obj.hero_image:
            return "-"
        return format_html(
            '<img src="{}" style="max-height: 200px; width: auto;" alt="{}" />',
            obj.hero_image.url,
            obj.title,
        )

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = list(super().get_readonly_fields(request, obj=obj))
        if obj:
            readonly_fields.append("key")
        return readonly_fields
