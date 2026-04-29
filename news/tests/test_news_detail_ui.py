from datetime import timedelta

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from news.models import Category, Post


class NewsDetailUITests(TestCase):
    def get_category(self, code, name):
        category, _ = Category.objects.get_or_create(
            code=code,
            defaults={"name": name},
        )
        return category

    def create_post(self, category, **overrides):
        defaults = {
            "category": category,
            "title": f"{category.name} 상세 테스트",
            "slug": f"{category.code}-detail-test",
            "content": "## 주요 안내\n\n본문 내용입니다.\n\n- 확인 항목",
            "is_published": True,
            "published_at": timezone.now() - timedelta(days=1),
        }
        defaults.update(overrides)
        return Post.objects.create(**defaults)

    def detail_response(self, post):
        return self.client.get(
            reverse(
                "news_detail",
                kwargs={
                    "category_code": post.category.code,
                    "slug": post.slug,
                },
            )
        )

    def test_detail_page_renders_premium_layout_for_each_news_category(self):
        cases = [
            ("notice", "공지사항", "별앤클래식의 공지사항과 입시 관련 소식을 확인하세요."),
            ("contest", "콩쿨정보", "피아노 콩쿨 일정과 준비에 필요한 정보를 확인하세요."),
            ("admission", "입시정보", "예중·예고 피아노 입시 준비에 필요한 정보를 확인하세요."),
        ]

        for code, name, summary in cases:
            with self.subTest(code=code):
                category = self.get_category(code, name)
                post = self.create_post(
                    category,
                    slug=f"{code}-detail-test",
                    title=f"{name} 상세 테스트",
                )

                response = self.detail_response(post)
                published_date = timezone.localtime(post.published_at).strftime("%Y.%m.%d")

                self.assertEqual(response.status_code, 200)
                html = response.content.decode("utf-8")
                self.assertIn('class="site-main news-detail-page"', html)
                self.assertIn('href="/static/css/layout_overrides.css"', html)
                self.assertIn("news-detail-hero", html)
                self.assertIn("news-detail-category-card", html)
                self.assertIn("news-detail-article-card", html)
                self.assertIn(summary, html)
                self.assertIn(f"{name} 상세 테스트", html)
                self.assertIn("작성일", html)
                self.assertIn(published_date, html)
                self.assertIn("작성자 관리자", html)
                self.assertIn("<h2>주요 안내</h2>", html)
                self.assertIn("목록으로 돌아가기", html)
                self.assertNotIn("콘텐츠 작성 영역", html)
                self.assertNotIn("게시글을 작성하거나 편집할 때 필요한 레이아웃 영역입니다.", html)

    def test_detail_page_hides_thumbnail_block_when_post_has_no_thumbnail(self):
        category = self.get_category("notice", "공지사항")
        post = self.create_post(category, slug="notice-no-thumbnail")

        response = self.detail_response(post)

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "news-detail-thumbnail")

    def test_detail_page_renders_thumbnail_when_post_has_thumbnail(self):
        category = self.get_category("contest", "콩쿨정보")
        post = self.create_post(
            category,
            slug="contest-with-thumbnail",
            thumbnail="news/thumbnails/contest.jpg",
        )

        response = self.detail_response(post)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "news-detail-thumbnail")
        self.assertContains(response, "/media/news/thumbnails/contest.jpg")
