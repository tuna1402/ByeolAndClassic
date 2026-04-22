from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("siteconfig", "0008_homeherovideo"),
    ]

    operations = [
        migrations.CreateModel(
            name="HomeFooterHero",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "image",
                    models.ImageField(
                        blank=True,
                        help_text="푸터 위 히어로 배경 이미지",
                        null=True,
                        upload_to="brand/home-footer/",
                    ),
                ),
                ("title", models.CharField(default="상담으로 시작하는 입시 준비", max_length=120)),
                (
                    "subtitle",
                    models.CharField(
                        default="맞춤형 커리큘럼 상담으로 목표 학교 합격 로드맵을 설계해보세요.",
                        max_length=220,
                    ),
                ),
                ("cta_label", models.CharField(default="상담 신청하기", max_length=50)),
                ("cta_url", models.CharField(default="/enroll/", max_length=200)),
                ("is_active", models.BooleanField(default=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "verbose_name": "홈 푸터 히어로",
                "verbose_name_plural": "홈 푸터 히어로",
                "ordering": ["-updated_at", "-created_at"],
            },
        ),
    ]
