import pytest
from django.urls import reverse
from django.utils import timezone

from news.models import Category, Post

pytestmark = pytest.mark.django_db


def test_home_renders_latest_news(client):
    category, _ = Category.objects.get_or_create(
        code="admission",
        defaults={"name": "입시정보"},
    )
    post = Post.objects.create(
        category=category,
        title="입시 일정 공지",
        slug="admission-news",
        content="테스트 콘텐츠",
        is_published=True,
        published_at=timezone.now(),
    )

    url = reverse("home")
    res = client.get(url)

    assert res.status_code == 200
    assert post.title in res.content.decode("utf-8")
