from django.shortcuts import render
from django.utils import timezone

from news.models import Post
from siteconfig.models import (
    AwardCertificate,
    HomeBannerSlide,
    HomeExamExpertImage,
    HomeFooterHero,
    HomeHeroVideo,
    RoadmapImageCard,
)

from .models import PageContent, PageKey


def home(request):
    now = timezone.now()
    base_queryset = Post.objects.filter(is_published=True, published_at__lte=now).select_related(
        "category"
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
    banner_slides = HomeBannerSlide.objects.filter(is_active=True).order_by("sort_order")[:5]
    roadmap_images = RoadmapImageCard.objects.filter(is_active=True).order_by("sort_order")
    awards = AwardCertificate.objects.filter(is_active=True).order_by("sort_order")
    exam_expert_images = HomeExamExpertImage.objects.filter(is_active=True).order_by("sort_order")[:3]
    hero_video = HomeHeroVideo.objects.filter(is_active=True).first()
    footer_hero = HomeFooterHero.objects.filter(is_active=True).first()
    return render(
        request,
        "pages/home.html",
        {
            "admission_latest": admission_latest,
            "contest_latest": contest_latest,
            "notice_latest": notice_latest,
            "banner_slides": banner_slides,
            "roadmap_images": roadmap_images,
            "awards": awards,
            "exam_expert_images": exam_expert_images,
            "hero_video": hero_video,
            "footer_hero": footer_hero,
        },
    )


def greeting(request):
    page = PageContent.objects.filter(key=PageKey.GREETING).first()
    return render(request, "pages/greeting.html", {"page": page})


def profile(request):
    page = PageContent.objects.filter(key=PageKey.PROFILE).first()
    return render(request, "pages/profile.html", {"page": page})


def awards(request):
    award_certificates = AwardCertificate.objects.filter(is_active=True).order_by("sort_order")
    return render(
        request,
        "pages/awards.html",
        {"award_certificates": award_certificates},
    )


def curriculum(request):
    page = PageContent.objects.filter(key=PageKey.CURRICULUM).first()
    curriculum_tracks = [
        {
            "key": "middle",
            "label": "예술중",
            "practice": [
                "기초 테크닉 확립 (HANON, Scale)",
                "입시 예비곡 레슨",
                "기초 바로크·고전 레퍼토리",
            ],
            "theory": ["시창·청음", "음악사"],
            "special": [],
        },
        {
            "key": "high",
            "label": "예술고",
            "practice": [
                "HANON Scale 암기",
                "입시곡 Lesson",
                "Bach Prelude & Fuga",
                "Chopin Etude op.10 / op.25",
            ],
            "theory": ["시창·청음", "음악사"],
            "special": [],
        },
        {
            "key": "college",
            "label": "예대",
            "practice": [
                "입시 지정곡·자유곡 집중 레슨",
                "Bach Prelude & Fuga 심화",
                "Chopin Etude op.10 / op.25 완성",
            ],
            "theory": ["시창·청음", "음악사", "건반화성"],
            "special": ["반주/반주법(가곡·기악 등)", "고전 소나타 1곡"],
        },
        {
            "key": "graduate",
            "label": "대학원",
            "practice": [
                "전공 실기 오디션/입시 레퍼토리 설계",
                "시대별 고난도 작품 완성도 향상",
                "심화 테크닉 및 무대 실전 코칭",
            ],
            "theory": ["시창·청음", "음악사", "건반화성"],
            "special": ["반주/반주법(가곡·기악 등)", "고전 소나타 1곡"],
        },
    ]
    lesson_policies = [
        {
            "icon": "fa-solid fa-ticket",
            "title": "차감제 운영",
            "description": "모든 레슨은 횟수 차감제로 운영됩니다.",
        },
        {
            "icon": "fa-regular fa-calendar-check",
            "title": "개별 맞춤 스케줄",
            "description": "입시 일정에 맞춰 개별 상담 후 수업 일정을 조율합니다.",
        },
        {
            "icon": "fa-regular fa-clock",
            "title": "48시간 취소 규정",
            "description": "수업 48시간 이내 취소 시 1회 차감될 수 있습니다.",
        },
        {
            "icon": "fa-solid fa-list-check",
            "title": "체계적 실기 관리",
            "description": "진단-계획-모의 실기 흐름으로 준비 과정을 관리합니다.",
        },
    ]
    return render(
        request,
        "pages/curriculum.html",
        {
            "page": page,
            "curriculum_tracks": curriculum_tracks,
            "default_track_key": "high",
            "lesson_policies": lesson_policies,
            "cta_url_name": "enroll_form",
        },
    )
