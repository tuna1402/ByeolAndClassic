from urllib.parse import urlencode

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
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
    if q:
        posts = posts.filter(Q(title__icontains=q) | Q(content__icontains=q))

    sort = request.GET.get("sort", "latest")
    if sort == "oldest":
        posts = posts.order_by("published_at", "created_at")
    else:
        sort = "latest"
        posts = posts.order_by("-published_at", "-created_at")

    paginator = Paginator(posts, 10)
    page_number = request.GET.get("page", 1)
    try:
        page_obj = paginator.page(page_number)
    except (EmptyPage, PageNotAnInteger):
        page_obj = paginator.page(1)

    query_params = {}
    if q:
        query_params["q"] = q
    if sort:
        query_params["sort"] = sort
    querystring = urlencode(query_params)

    context = {
        "category": category,
        "page_obj": page_obj,
        "paginator": paginator,
        "q": q,
        "sort": sort,
        "querystring": querystring,
    }
    return render(request, "news/list.html", context)


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
