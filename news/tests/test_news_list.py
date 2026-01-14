from datetime import timedelta

import pytest
from django.urls import reverse
from django.utils import timezone

from news.models import Category, Post

pytestmark = pytest.mark.django_db


def create_category():
    category, _ = Category.objects.get_or_create(
        code="notice",
        defaults={"name": "공지사항"},
    )
    return category


def create_posts(category, total=15):
    now = timezone.now()
    posts = []
    for i in range(total):
        posts.append(
            Post.objects.create(
                category=category,
                title=f"post {i}",
                slug=f"post-{i}",
                content="내용입니다.",
                is_published=True,
                published_at=now - timedelta(days=i),
            )
        )
    return posts


def test_news_list_pagination(client):
    category = create_category()
    create_posts(category)

    url = reverse("news_category", kwargs={"category_code": category.code})
    res = client.get(url)
    assert res.status_code == 200
    assert len(res.context["page_obj"].object_list) == 10

    res_page_two = client.get(url, {"page": 2})
    assert len(res_page_two.context["page_obj"].object_list) == 5


def test_news_list_search(client):
    category = create_category()
    create_posts(category, total=3)
    Post.objects.create(
        category=category,
        title="피아노 콩쿨 소식",
        slug="piano-news",
        content="피아노 관련 안내입니다.",
        is_published=True,
        published_at=timezone.now(),
    )

    url = reverse("news_category", kwargs={"category_code": category.code})
    res = client.get(url, {"q": "피아노"})
    assert res.status_code == 200
    titles = [post.title for post in res.context["page_obj"].object_list]
    assert titles == ["피아노 콩쿨 소식"]


def test_news_list_sort_oldest(client):
    category = create_category()
    create_posts(category)

    url = reverse("news_category", kwargs={"category_code": category.code})
    res = client.get(url, {"sort": "oldest"})
    assert res.status_code == 200
    first_post = res.context["page_obj"].object_list[0]
    assert first_post.slug == "post-14"
