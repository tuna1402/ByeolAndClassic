from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from news.models import Category, Post


class HomeLatestNewsTests(TestCase):
    def setUp(self):
        self.admission, _ = Category.objects.get_or_create(code="admission", name="입시정보")
        self.contest, _ = Category.objects.get_or_create(code="contest", name="콩쿨정보")
        self.notice, _ = Category.objects.get_or_create(code="notice", name="공지사항")

    def test_home_renders_latest_news(self):
        now = timezone.now()
        admission_post = Post.objects.create(
            category=self.admission,
            title="입시 소식",
            slug="admission-news",
            content="입시 안내",
            is_published=True,
            published_at=now,
        )
        contest_post = Post.objects.create(
            category=self.contest,
            title="콩쿨 소식",
            slug="contest-news",
            content="콩쿨 안내",
            is_published=True,
            published_at=now,
        )
        notice_post = Post.objects.create(
            category=self.notice,
            title="공지 안내",
            slug="notice-news",
            content="공지 안내",
            is_published=True,
            published_at=now,
        )

        response = self.client.get(reverse("home"))
        self.assertContains(response, admission_post.title)
        self.assertContains(response, contest_post.title)
        self.assertContains(response, notice_post.title)
