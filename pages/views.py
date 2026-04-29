from siteconfig.models import HomeHeroVideo
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
            "goal": [
                "기초 테크닉과 음악적 표현력의 균형 형성",
                "목표 학교 유형에 맞춘 입시 준비 방향 설정",
                "무대 경험을 통한 자신감과 집중력 관리",
            ],
            "practice": [
                "기초 테크닉 확립 (HANON, Scale)",
                "입시 예비곡 레슨",
                "기초 바로크·고전 레퍼토리",
            ],
            "theory": ["시창·청음 기초 훈련", "음악사 핵심 흐름 정리"],
            "period": ["초등 고학년: 최소 12개월 이상", "목표 학교별 실기 유형 확인 후 계획 수립"],
        },
        {
            "key": "high",
            "label": "예술고",
            "goal": [
                "실기 역량 강화 및 음악적 표현력 완성",
                "학교별 입시 유형에 맞춘 맞춤 준비",
                "자신감 있는 무대 경험과 멘탈 관리",
            ],
            "practice": [
                "테크닉 및 터치, 음색 컨트롤 집중 지도",
                "곡 해석과 구조 이해를 통한 완성도 향상",
                "Bach Prelude & Fuga",
                "Chopin Etude op.10 / op.25",
            ],
            "theory": ["시창·청음 집중 훈련", "화성·음악사 핵심 개념 정리"],
            "period": ["예술고 1학년: 최소 12개월 이상", "예술고 2~3학년: 18개월 이상 권장"],
        },
        {
            "key": "college",
            "label": "예대",
            "goal": [
                "전공 실기 평가 기준에 맞춘 레퍼토리 설계",
                "작품별 스타일과 구조 해석 심화",
                "실전 모의 실기를 통한 완성도 점검",
            ],
            "practice": [
                "입시 지정곡·자유곡 집중 레슨",
                "Bach Prelude & Fuga 심화",
                "Chopin Etude op.10 / op.25 완성",
            ],
            "theory": ["시창·청음 심화", "음악사·건반화성 핵심 정리", "반주법 기초 점검"],
            "period": ["고2 이후: 18개월 이상 권장", "지원 학교별 지정곡 발표 일정에 맞춰 조정"],
        },
        {
            "key": "graduate",
            "label": "대학원",
            "goal": [
                "전공 방향에 맞는 고급 레퍼토리 구성",
                "논리적인 작품 해석과 무대 설득력 강화",
                "오디션 및 면접 흐름까지 고려한 준비",
            ],
            "practice": [
                "전공 실기 오디션/입시 레퍼토리 설계",
                "시대별 고난도 작품 완성도 향상",
                "심화 테크닉 및 무대 실전 코칭",
            ],
            "theory": ["음악사·화성 흐름 정리", "전공 면접 대비 개념 점검", "반주 및 앙상블 역량 보완"],
            "period": ["입시 12~18개월 전 상담 권장", "레퍼토리 규모에 따라 장기 계획 수립"],
        },
    ]
    roadmap_steps = [
        {
            "number": "01",
            "icon": "fa-solid fa-magnifying-glass",
            "title": "현재 수준 진단",
            "description": "실력 진단과 성향 파악",
        },
        {
            "number": "02",
            "icon": "fa-solid fa-bullseye",
            "title": "목표 설정",
            "description": "목표 학교 및 방향 설정",
        },
        {
            "number": "03",
            "icon": "fa-solid fa-music",
            "title": "입시곡 선정",
            "description": "학교별 맞춤 곡 선정",
        },
        {
            "number": "04",
            "icon": "fa-solid fa-list-check",
            "title": "실기 완성도 관리",
            "description": "정기 레슨 및 피드백",
        },
        {
            "number": "05",
            "icon": "fa-solid fa-check",
            "title": "모의 실기 점검",
            "description": "실전 모의 실기로 최종 점검",
        },
    ]
    lesson_policies = [
        {
            "icon": "fa-solid fa-calendar-days",
            "title": "개인 일정에 맞춘 자율제 운영",
            "description": "학생의 스케줄에 맞춰 유연하게 수업을 운영합니다.",
        },
        {
            "icon": "fa-regular fa-calendar-check",
            "title": "입시 일정에 맞춘 개별 스케줄",
            "description": "입시 일정과 목표에 맞춰 맞춤형 스케줄을 제공합니다.",
        },
        {
            "icon": "fa-regular fa-clock",
            "title": "48시간 취소 규정",
            "description": "수업 48시간 이전 취소 시 1회 차감은 없습니다.",
        },
        {
            "icon": "fa-solid fa-star",
            "title": "입시곡 완성도 중심 실기 관리",
            "description": "곡의 완성도와 음악적 표현을 중심으로 체계적으로 관리합니다.",
        },
    ]
    pricing_options = [
        {
            "title": "입시 레슨",
            "duration": "50분",
            "price": "120,000원",
            "recommended_for": "입시곡 완성도를 높이고 싶은 학생",
        },
        {
            "title": "레벨 테스트",
            "duration": "30분",
            "price": "20,000원",
            "recommended_for": "현재 실력과 방향을 진단받고 싶은 학생",
        },
        {
            "title": "입시 컨설팅",
            "duration": "40분",
            "price": "50,000원",
            "recommended_for": "진학 계획 및 입시 전략 상담이 필요한 학생",
        },
    ]
    curriculum_faqs = [
        {
            "question": "예중 피아노 입시는 언제부터 준비하면 좋을까요?",
            "answer": "학생의 현재 실력과 목표 학교에 따라 다르지만, 기본기와 입시곡 완성도를 고려해 충분한 준비 기간을 두는 것이 좋습니다.",
        },
        {
            "question": "입시곡은 어려운 곡이 유리한가요?",
            "answer": "곡의 난이도보다 학생에게 맞는 곡을 완성도 있게 연주하는 것이 더 중요합니다.",
        },
        {
            "question": "레벨 테스트는 어떻게 진행되나요?",
            "answer": "현재 연주 수준, 기본기, 음악 표현, 준비 기간을 함께 확인해 입시 준비 방향을 안내합니다.",
        },
        {
            "question": "수업은 주 몇 회 진행되나요?",
            "answer": "학생의 목표와 준비 상황에 따라 상담 후 조정합니다.",
        },
    ]
    return render(
        request,
        "pages/curriculum.html",
        {
            "page": page,
            "curriculum_tracks": curriculum_tracks,
            "default_track_key": "high",
            "roadmap_steps": roadmap_steps,
            "lesson_policies": lesson_policies,
            "pricing_options": pricing_options,
            "curriculum_faqs": curriculum_faqs,
            "cta_url_name": "enroll_form",
        },
    )


def academy_video(request):
    hero_video = HomeHeroVideo.objects.filter(is_active=True).first()
    return render(
        request,
        "pages/video_intro.html",
        {
            "hero_video": hero_video,
        },
    )
