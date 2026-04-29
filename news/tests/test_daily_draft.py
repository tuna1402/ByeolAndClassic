from datetime import date

from django.test import TestCase

from news.models import Post
from news.utils.daily_draft import (
    build_daily_draft_spec,
    create_daily_draft_for_date,
    select_board_code_for_date,
)


class DailyDraftTests(TestCase):
    def test_select_board_code_rotates_from_base_date(self):
        self.assertEqual(select_board_code_for_date(date(2024, 1, 1)), "notice")
        self.assertEqual(select_board_code_for_date(date(2024, 1, 2)), "contest")
        self.assertEqual(select_board_code_for_date(date(2024, 1, 3)), "admission")
        self.assertEqual(select_board_code_for_date(date(2024, 1, 4)), "notice")

    def test_build_daily_draft_spec_uses_date_slug_and_default_thumbnail(self):
        spec = build_daily_draft_spec(date(2024, 1, 3))

        self.assertEqual(spec.board_code, "admission")
        self.assertEqual(spec.slug, "admission-2024-01-03")
        self.assertEqual(spec.thumbnail, "defaults/default_admission.jpg")
        self.assertIn("오늘의 입시 주제", spec.content)

    def test_create_daily_draft_creates_unpublished_post(self):
        result = create_daily_draft_for_date(date(2024, 1, 2))

        self.assertTrue(result.created)
        post = Post.objects.get(slug="contest-2024-01-02")
        self.assertEqual(post.category.code, "contest")
        self.assertFalse(post.is_published)
        self.assertEqual(post.thumbnail.name, "defaults/default_contest.jpg")
        self.assertIn("콩쿨명", post.content)

    def test_create_daily_draft_does_not_duplicate_same_slug(self):
        first = create_daily_draft_for_date(date(2024, 1, 1))
        second = create_daily_draft_for_date(date(2024, 1, 1))

        self.assertTrue(first.created)
        self.assertFalse(second.created)
        self.assertEqual(first.post.pk, second.post.pk)
        self.assertEqual(Post.objects.filter(slug="notice-2024-01-01").count(), 1)
