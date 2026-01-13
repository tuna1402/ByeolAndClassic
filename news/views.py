from django.shortcuts import get_object_or_404, render
from django.utils import timezone

from .models import Category, Post


def category_list(request, category_code):
    category = get_object_or_404(Category, code=category_code)
    now = timezone.now()
    posts = (
        category.posts.filter(is_published=True, published_at__lte=now)
        .select_related("category")
    )
    return render(request, "news/list.html", {"category": category, "posts": posts})


def detail(request, category_code, slug):
    now = timezone.now()
    post = get_object_or_404(
        Post,
        category__code=category_code,
        slug=slug,
        is_published=True,
        published_at__lte=now,
    )
    return render(request, "news/detail.html", {"post": post})
