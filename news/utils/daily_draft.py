from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Final

from django.utils import timezone

from news.models import Category, Post

DAILY_DRAFT_BASE_DATE: Final[date] = date(2024, 1, 1)

BOARD_SEQUENCE: Final[tuple[str, ...]] = ("notice", "contest", "admission")

BOARD_LABELS: Final[dict[str, str]] = {
    "notice": "공지사항",
    "contest": "콩쿨정보",
    "admission": "입시정보",
}

DEFAULT_THUMBNAILS: Final[dict[str, str]] = {
    "notice": "defaults/default_notice.jpg",
    "contest": "defaults/default_contest.jpg",
    "admission": "defaults/default_admission.jpg",
}

CONTENT_TEMPLATES: Final[dict[str, str]] = {
    "notice": """## 오늘의 공지 주제

- 작성 예정

## 대상

- 작성 예정

## 안내 내용

- 작성 예정

## 운영자가 확인할 사항

- 작성 예정

## 공개 전 체크리스트

- [ ] 제목 확인
- [ ] 대상 확인
- [ ] 일정 및 표현 확인""",
    "contest": """## 콩쿨명

- 작성 예정

## 주최/주관

- 작성 예정

## 접수 기간

- 작성 예정

## 대회 일정

- 작성 예정

## 참가 대상

- 작성 예정

## 피아노 부문

- 작성 예정

## 공식 출처

- 작성 예정

## 첨부파일 확인

- 작성 예정

## 광주 피아노 입시생 관점에서 확인할 점

- 작성 예정

## 공개 전 체크리스트

- [ ] 공식 공고 링크 확인
- [ ] 접수 기간 확인
- [ ] 참가 대상 및 부문 확인
- [ ] 첨부파일 확인""",
    "admission": """## 오늘의 입시 주제

- 작성 예정

## 광주 피아노 입시 핵심 포인트

- 작성 예정

## 예중/예고 피아노 입시 준비 방향

- 작성 예정

## 학생 현재 수준 점검

- 작성 예정

## 피아노 실기 준비 포인트

- 작성 예정

## 연습 루틴 점검

- 작성 예정

## 공개 전 체크리스트

- [ ] 학교명 및 전형 확인
- [ ] 실기곡 기준 확인
- [ ] 일정 확인
- [ ] 학생 수준별 표현 확인""",
}


@dataclass(frozen=True)
class DailyDraftSpec:
    target_date: date
    board_code: str
    board_label: str
    slug: str
    title: str
    content: str
    thumbnail: str


@dataclass(frozen=True)
class DailyDraftCreationResult:
    spec: DailyDraftSpec
    post: Post
    created: bool


def select_board_code_for_date(
    target_date: date,
    base_date: date = DAILY_DRAFT_BASE_DATE,
) -> str:
    day_offset = (target_date - base_date).days
    return BOARD_SEQUENCE[day_offset % len(BOARD_SEQUENCE)]


def build_daily_draft_slug(board_code: str, target_date: date) -> str:
    return f"{board_code}-{target_date:%Y-%m-%d}"


def build_daily_draft_spec(
    target_date: date,
    base_date: date = DAILY_DRAFT_BASE_DATE,
) -> DailyDraftSpec:
    board_code = select_board_code_for_date(target_date, base_date=base_date)
    board_label = BOARD_LABELS[board_code]
    slug = build_daily_draft_slug(board_code, target_date)
    return DailyDraftSpec(
        target_date=target_date,
        board_code=board_code,
        board_label=board_label,
        slug=slug,
        title=f"{target_date:%Y-%m-%d} {board_label} 초안",
        content=CONTENT_TEMPLATES[board_code],
        thumbnail=DEFAULT_THUMBNAILS[board_code],
    )


def create_daily_draft_for_date(target_date: date | None = None) -> DailyDraftCreationResult:
    draft_date = target_date or timezone.localdate()
    spec = build_daily_draft_spec(draft_date)

    existing_post = Post.objects.filter(slug=spec.slug).first()
    if existing_post is not None:
        return DailyDraftCreationResult(spec=spec, post=existing_post, created=False)

    category, _ = Category.objects.get_or_create(
        code=spec.board_code,
        defaults={"name": spec.board_label},
    )
    post = Post.objects.create(
        category=category,
        title=spec.title,
        slug=spec.slug,
        content=spec.content,
        thumbnail=spec.thumbnail,
        is_published=False,
    )
    return DailyDraftCreationResult(spec=spec, post=post, created=True)
