from django.shortcuts import render
from django.utils import timezone

from news.models import Post

from .models import PageContent, PageKey


def home(request):
    now = timezone.now()
    base_queryset = Post.objects.filter(is_published=True, published_at__lte=now).select_related(
        "category"
    )
    admission_latest = (
        base_queryset.filter(category__code="admission")
        .order_by("-published_at", "-created_at")[:5]
    )
    contest_latest = (
        base_queryset.filter(category__code="contest")
        .order_by("-published_at", "-created_at")[:3]
    )
    notice_latest = (
        base_queryset.filter(category__code="notice")
        .order_by("-published_at", "-created_at")[:3]
    )
    return render(
        request,
        "pages/home.html",
        {
            "admission_latest": admission_latest,
            "contest_latest": contest_latest,
            "notice_latest": notice_latest,
        },
    )


def greeting(request):
    page = PageContent.objects.filter(key=PageKey.GREETING).first()
    return render(request, "pages/greeting.html", {"page": page})


def profile(request):
    page = PageContent.objects.filter(key=PageKey.PROFILE).first()
    return render(request, "pages/profile.html", {"page": page})


def awards(request):
    page = PageContent.objects.filter(key=PageKey.AWARDS).first()
    return render(request, "pages/awards.html", {"page": page})


def curriculum(request):
    page = PageContent.objects.filter(key=PageKey.CURRICULUM).first()
    return render(request, "pages/curriculum.html", {"page": page})


def accompanist(request):
    page = PageContent.objects.filter(key=PageKey.ACCOMPANIST).first()
    return render(request, "pages/accompanist.html", {"page": page})


def soloist(request):
    page = PageContent.objects.filter(key=PageKey.SOLOIST).first()
    return render(request, "pages/soloist.html", {"page": page})


def masterclass(request):
    page = PageContent.objects.filter(key=PageKey.MASTERCLASS).first()
    return render(request, "pages/masterclass.html", {"page": page})
