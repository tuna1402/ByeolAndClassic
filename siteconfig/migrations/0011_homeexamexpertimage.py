from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("siteconfig", "0010_awardcertificate_year"),
    ]

    operations = [
        migrations.CreateModel(
            name="HomeExamExpertImage",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "image",
                    models.ImageField(
                        help_text="홈 입시 전문가 섹션 이미지. 권장: 900x1200",
                        upload_to="brand/home-exam-expert/",
                    ),
                ),
                ("alt_text", models.CharField(blank=True, max_length=120)),
                ("is_active", models.BooleanField(default=True)),
                ("sort_order", models.PositiveSmallIntegerField(default=1)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "verbose_name": "홈 입시 전문가 이미지",
                "verbose_name_plural": "홈 입시 전문가 이미지",
                "ordering": ["sort_order", "-created_at"],
            },
        ),
    ]
