from django.db.models import Q
from django.shortcuts import render
from django.utils import timezone

from .models import PageContent, PageKey
from news.models import Post


def home(request):
    now = timezone.now()
    published_filter = Q(published_at__isnull=True) | Q(published_at__lte=now)
    base_queryset = (
        Post.objects.filter(is_published=True)
        .filter(published_filter)
        .select_related("category")
    )
    admission_latest = (
        base_queryset.filter(category__code="admission")
        .order_by("-published_at", "-created_at")[:3]
    )
    contest_latest = (
        base_queryset.filter(category__code="contest")
        .order_by("-published_at", "-created_at")[:3]
    )
    notice_latest = (
        base_queryset.filter(category__code="notice")
        .order_by("-published_at", "-created_at")[:3]
    )
    context = {
        "admission_latest": admission_latest,
        "contest_latest": contest_latest,
        "notice_latest": notice_latest,
    }
    return render(request, "pages/home.html", context)


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
