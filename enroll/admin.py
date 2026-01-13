from django.contrib import admin

from enroll.models import EnrollApplication


@admin.register(EnrollApplication)
class EnrollApplicationAdmin(admin.ModelAdmin):
    list_display = ("name", "phone", "preferred_date", "is_handled", "created_at")
    list_filter = ("is_handled", "preferred_date")
    search_fields = ("name", "phone")
    readonly_fields = ("created_at", "updated_at")
