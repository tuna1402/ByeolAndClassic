from datetime import timedelta

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify

from news.models import Category, Post


class NewsListTests(TestCase):
    def setUp(self):
        self.category, _ = Category.objects.get_or_create(code="notice", name="공지사항")

    def create_post(self, title, content="", published_at=None, slug=None):
        if slug is None:
            slug = slugify(title)
            if not slug:
                slug = f"post-{Post.objects.count() + 1}"
        return Post.objects.create(
            category=self.category,
            title=title,
            slug=slug,
            content=content,
            is_published=True,
            published_at=published_at or timezone.now(),
        )

    def test_pagination(self):
        now = timezone.now()
        for i in range(15):
            self.create_post(title=f"게시글 {i}", published_at=now - timedelta(days=i))

        response = self.client.get(
            reverse("news_category", kwargs={"category_code": self.category.code})
        )
        page_obj = response.context["page_obj"]
        self.assertEqual(page_obj.paginator.count, 15)
        self.assertEqual(len(page_obj.object_list), 10)

        response_page2 = self.client.get(
            reverse("news_category", kwargs={"category_code": self.category.code}),
            {"page": 2},
        )
        page_obj_page2 = response_page2.context["page_obj"]
        self.assertEqual(len(page_obj_page2.object_list), 5)

    def test_search_query(self):
        self.create_post(title="입시 일정 안내", content="입시 계획 공유")
        self.create_post(title="기타 소식", content="대회 안내")

        response = self.client.get(
            reverse("news_category", kwargs={"category_code": self.category.code}),
            {"q": "입시"},
        )
        page_obj = response.context["page_obj"]
        self.assertEqual(page_obj.paginator.count, 1)
        self.assertEqual(page_obj.object_list[0].title, "입시 일정 안내")

    def test_sort_oldest(self):
        now = timezone.now()
        newest = self.create_post(title="최신 글", published_at=now)
        oldest = self.create_post(title="오래된 글", published_at=now - timedelta(days=10))

        response = self.client.get(
            reverse("news_category", kwargs={"category_code": self.category.code}),
            {"sort": "oldest"},
        )
        page_obj = response.context["page_obj"]
        self.assertEqual(page_obj.object_list[0].id, oldest.id)
        self.assertEqual(page_obj.object_list[1].id, newest.id)
