from datetime import timedelta

from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from django.utils import timezone

from .models import Category, Post
from .utils import render_markdown_safe


GUIDE_TAB_CONFIG = {
    "competition": {
        "category_code": "contest",
        "label": "콩쿨",
        "hero_image": "images/home/home-news-award.png",
        "feature_image": "images/home/home-news-award.png",
        "fallback_title": "2026 하반기 주요 콩쿨 일정 & 준비 가이드",
        "fallback_description": "전국 주요 콩쿨의 일정과 특징, 준비 포인트를 한눈에 정리했습니다.",
        "fallback_cards": [
            {
                "title": "여름방학 콩쿨 준비 체크리스트",
                "summary": "연습량, 리허설, 의상과 당일 동선을 미리 점검합니다.",
                "icon": "fa-solid fa-list-check",
            },
            {
                "title": "콩쿨 당일 무대 리허설 가이드",
                "summary": "무대 적응과 첫 음 집중을 위한 실전 루틴을 정리합니다.",
                "icon": "fa-solid fa-person-chalkboard",
            },
            {
                "title": "콩쿨곡 선택 전략",
                "summary": "학생의 강점과 심사 기준을 함께 고려해 레퍼토리를 설계합니다.",
                "icon": "fa-solid fa-music",
            },
        ],
    },
    "admission": {
        "category_code": "admission",
        "label": "입시",
        "hero_image": "images/home/home-news-piano.png",
        "feature_image": "images/home/home-news-piano.png",
        "fallback_title": "2026 예중·예고 피아노 입시 준비 로드맵",
        "fallback_description": "목표 학교와 현재 실력에 맞춘 입시곡, 연습 계획, 실전 점검 흐름을 안내합니다.",
        "fallback_cards": [
            {
                "title": "예중 입시 준비 시작 전 확인할 것",
                "summary": "기초 테크닉, 음악성, 목표 학교 유형을 먼저 점검합니다.",
                "icon": "fa-solid fa-school",
            },
            {
                "title": "예고 입시 곡 구성과 연습 계획",
                "summary": "실기곡 난이도와 완성도를 기준으로 기간별 연습을 설계합니다.",
                "icon": "fa-solid fa-calendar-check",
            },
            {
                "title": "음대 입시 레퍼토리 계획 세우기",
                "summary": "시대별 작품 균형과 학생의 표현 강점을 함께 반영합니다.",
                "icon": "fa-solid fa-book-open",
            },
            {
                "title": "실기 전형 체크리스트",
                "summary": "전형 일정, 제출 서류, 모의 실기 점검 항목을 정리합니다.",
                "icon": "fa-solid fa-clipboard-check",
            },
            {
                "title": "청음·시창 대비 전략",
                "summary": "실기 준비와 병행할 수 있는 기초 이론 루틴을 안내합니다.",
                "icon": "fa-solid fa-headphones",
            },
            {
                "title": "입시 상담 전 준비할 질문",
                "summary": "현재 수준, 목표 학교, 준비 기간을 기준으로 상담 내용을 정리합니다.",
                "icon": "fa-regular fa-comments",
            },
        ],
    },
}


def _published_posts(category):
    now = timezone.now()
    published_filter = Q(published_at__isnull=True) | Q(published_at__lte=now)
    return (
        category.posts.filter(is_published=True)
        .filter(published_filter)
        .select_related("category")
    )


def _apply_search_and_sort(posts, request):
    q = request.GET.get("q", "").strip()
    sort = request.GET.get("sort", "latest")
    if q:
        posts = posts.filter(Q(title__icontains=q) | Q(content__icontains=q))
    if sort == "oldest":
        posts = posts.order_by("published_at", "created_at")
    else:
        posts = posts.order_by("-published_at", "-created_at")
    return posts, q, sort


def _querystring_without_page(request):
    query_params = request.GET.copy()
    query_params.pop("page", None)
    return query_params.urlencode()


def _new_post_ids(posts):
    threshold = timezone.now() - timedelta(days=7)
    return [
        post.id
        for post in posts
        if (post.published_at or post.created_at) and (post.published_at or post.created_at) >= threshold
    ]


def notice_list(request):
    category = get_object_or_404(Category, code="notice")
    posts, q, sort = _apply_search_and_sort(_published_posts(category), request)

    paginator = Paginator(posts, 10)
    page_obj = paginator.get_page(request.GET.get("page"))
    featured_post = _published_posts(category).order_by("-published_at", "-created_at").first()

    return render(
        request,
        "news/notice_list.html",
        {
            "category": category,
            "page_obj": page_obj,
            "featured_post": featured_post,
            "new_post_ids": _new_post_ids(page_obj.object_list),
            "q": q,
            "sort": sort,
            "querystring": _querystring_without_page(request),
        },
    )


def guide_info(request, forced_tab=None):
    tab = forced_tab or request.GET.get("tab", "competition")
    if tab == "contest":
        tab = "competition"
    if tab not in GUIDE_TAB_CONFIG:
        tab = "competition"

    tab_config = GUIDE_TAB_CONFIG[tab]
    category = get_object_or_404(Category, code=tab_config["category_code"])
    posts, q, sort = _apply_search_and_sort(_published_posts(category), request)
    feature_post = posts.first()
    card_posts = posts.exclude(pk=feature_post.pk) if feature_post else posts

    paginator = Paginator(card_posts, 6)
    page_obj = paginator.get_page(request.GET.get("page"))

    return render(
        request,
        "news/guide_info.html",
        {
            "active_tab": tab,
            "category": category,
            "feature_post": feature_post,
            "page_obj": page_obj,
            "q": q,
            "sort": sort,
            "querystring": _querystring_without_page(request),
            "tab_config": tab_config,
            "competition_tab_config": GUIDE_TAB_CONFIG["competition"],
            "admission_tab_config": GUIDE_TAB_CONFIG["admission"],
        },
    )


def category_list(request, category_code):
    category = get_object_or_404(Category, code=category_code)
    if category.code == "notice":
        return notice_list(request)
    if category.code == "contest":
        return guide_info(request, forced_tab="competition")
    if category.code == "admission":
        return guide_info(request, forced_tab="admission")

    posts, q, sort = _apply_search_and_sort(_published_posts(category), request)

    paginator = Paginator(posts, 10)
    page_obj = paginator.get_page(request.GET.get("page"))

    return render(
        request,
        "news/list.html",
        {
            "category": category,
            "page_obj": page_obj,
            "q": q,
            "sort": sort,
            "querystring": _querystring_without_page(request),
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
    post_html = render_markdown_safe(post.content)
    return render(
        request,
        "news/detail.html",
        {
            "post": post,
            "post_html": post_html,
        },
    )
