from django.contrib import admin, messages
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.urls import path, reverse
from django.utils import timezone

from .models import Category, Post
from .utils.daily_draft import create_daily_draft_for_date


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("code", "name")
    search_fields = ("code", "name")


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    change_list_template = "admin/news/post/change_list.html"
    list_display = ("title", "slug", "category", "is_published", "published_at", "created_at")
    list_filter = ("category", "is_published")
    search_fields = ("title", "slug", "content")
    prepopulated_fields = {"slug": ("title",)}
    date_hierarchy = "published_at"
    list_select_related = ("category",)

    def save_model(self, request, obj, form, change):
        if obj.is_published and obj.published_at is None:
            obj.published_at = timezone.now()
        super().save_model(request, obj, form, change)

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "create-today-draft/",
                self.admin_site.admin_view(self.create_today_draft),
                name="news_post_create_today_draft",
            ),
        ]
        return custom_urls + urls

    def create_today_draft(self, request):
        if not self.has_add_permission(request):
            raise PermissionDenied

        changelist_url = reverse("admin:news_post_changelist")
        if request.method != "POST":
            messages.warning(request, "오늘의 초안 생성 버튼으로 실행해 주세요.")
            return redirect(changelist_url)

        result = create_daily_draft_for_date()
        if result.created:
            messages.success(
                request,
                f"{result.spec.board_label} 오늘의 초안이 생성되었습니다. slug: {result.spec.slug}",
            )
        else:
            messages.warning(
                request,
                f"{result.spec.board_label} 오늘의 초안이 이미 존재합니다. "
                f"중복 생성하지 않았습니다. slug: {result.spec.slug}",
            )
        return redirect(changelist_url)
