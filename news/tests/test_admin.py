from datetime import datetime
from unittest.mock import patch

from django.contrib.admin.sites import AdminSite
from django.test import RequestFactory, TestCase
from django.utils import timezone

from news.admin import PostAdmin
from news.models import Category, Post


class PostAdminSaveModelTests(TestCase):
    def setUp(self):
        self.category, _ = Category.objects.get_or_create(
            code="notice",
            defaults={"name": "공지사항"},
        )
        self.admin = PostAdmin(Post, AdminSite())
        self.request = RequestFactory().post("/admin/news/post/add/")

    def make_post(self, **overrides):
        defaults = {
            "category": self.category,
            "title": "테스트 글",
            "slug": f"test-post-{Post.objects.count() + 1}",
            "content": "테스트 내용",
        }
        defaults.update(overrides)
        return Post(**defaults)

    def test_sets_published_at_when_admin_publishes_without_date(self):
        now = timezone.make_aware(datetime(2026, 4, 30, 12, 0))
        post = self.make_post(is_published=True, published_at=None)

        with patch("news.admin.timezone.now", return_value=now):
            self.admin.save_model(self.request, post, form=None, change=False)

        post.refresh_from_db()
        self.assertEqual(post.published_at, now)

    def test_does_not_overwrite_existing_published_at(self):
        existing_published_at = timezone.make_aware(datetime(2026, 4, 1, 9, 30))
        now = timezone.make_aware(datetime(2026, 4, 30, 12, 0))
        post = self.make_post(
            is_published=True,
            published_at=existing_published_at,
        )

        with patch("news.admin.timezone.now", return_value=now):
            self.admin.save_model(self.request, post, form=None, change=False)

        post.refresh_from_db()
        self.assertEqual(post.published_at, existing_published_at)

    def test_does_not_set_published_at_for_unpublished_post(self):
        now = timezone.make_aware(datetime(2026, 4, 30, 12, 0))
        post = self.make_post(is_published=False, published_at=None)

        with patch("news.admin.timezone.now", return_value=now):
            self.admin.save_model(self.request, post, form=None, change=False)

        post.refresh_from_db()
        self.assertIsNone(post.published_at)
