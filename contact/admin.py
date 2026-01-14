from django.contrib import admin

from contact.models import ContactMessage


@admin.action(description="선택 문의를 처리 완료로 표시")
def mark_handled(modeladmin, request, queryset):
    queryset.update(is_handled=True)


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "phone", "email", "is_handled", "created_at")
    list_filter = ("is_handled", "created_at")
    search_fields = ("name", "phone", "email", "message", "memo")
    readonly_fields = ("created_at", "updated_at")
    actions = [mark_handled]
