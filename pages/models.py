from django.db import models


class PageKey(models.TextChoices):
    GREETING = "greeting", "인삿말"
    PROFILE = "profile", "프로필"
    AWARDS = "awards", "수상내역"
    CURRICULUM = "curriculum", "커리큘럼"
    ACCOMPANIST = "accompanist", "반주자 매칭"
    SOLOIST = "soloist", "솔리스트 매칭"
    MASTERCLASS = "masterclass", "마스터 클래스"


class PageContent(models.Model):
    key = models.SlugField(
        unique=True,
        choices=PageKey.choices,
        help_text="페이지 고유 키입니다. 신규 생성 시에만 설정하세요.",
    )
    title = models.CharField(max_length=200)
    content = models.TextField(blank=True)
    hero_image = models.ImageField(upload_to="pages/hero/", blank=True, null=True)
    attachment = models.FileField(upload_to="pages/files/", blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["key"]

    def __str__(self) -> str:
        return self.title or self.key
