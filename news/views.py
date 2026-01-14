from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from django.utils import timezone

from .models import Category, Post


def category_list(request, category_code):
    category = get_object_or_404(Category, code=category_code)
    now = timezone.now()
    published_filter = Q(published_at__isnull=True) | Q(published_at__lte=now)
    posts = (
        category.posts.filter(is_published=True)
        .filter(published_filter)
        .select_related("category")
    )
    q = request.GET.get("q", "").strip()
    sort = request.GET.get("sort", "latest")
    if q:
        posts = posts.filter(Q(title__icontains=q) | Q(content__icontains=q))
    if sort == "oldest":
        posts = posts.order_by("published_at", "created_at")
    else:
        posts = posts.order_by("-published_at", "-created_at")

    paginator = Paginator(posts, 10)
    page_obj = paginator.get_page(request.GET.get("page"))
    query_params = request.GET.copy()
    query_params.pop("page", None)
    querystring = query_params.urlencode()

    return render(
        request,
        "news/list.html",
        {
            "category": category,
            "page_obj": page_obj,
            "q": q,
            "sort": sort,
            "querystring": querystring,
        },
    )


def detail(request, category_code, slug):
    now = timezone.now()
    published_filter = Q(published_at__isnull=True) | Q(published_at__lte=now)
    post = get_object_or_404(
        Post.objects.filter(published_filter),
        category__code=category_code,
        slug=slug,
        is_published=True,
    )
    return render(request, "news/detail.html", {"post": post})
