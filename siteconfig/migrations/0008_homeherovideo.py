from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("siteconfig", "0007_delete_sitebrandsettings"),
    ]

    operations = [
        migrations.CreateModel(
            name="HomeHeroVideo",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "video",
                    models.FileField(
                        help_text="홈 히어로 mp4 영상 (권장 1920x780)",
                        upload_to="brand/home-hero/",
                    ),
                ),
                ("title", models.CharField(blank=True, max_length=120)),
                ("is_active", models.BooleanField(default=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "verbose_name": "홈 히어로 영상",
                "verbose_name_plural": "홈 히어로 영상",
                "ordering": ["-updated_at", "-created_at"],
            },
        ),
    ]
