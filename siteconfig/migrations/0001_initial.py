from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="SiteBrandSettings",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("site_name", models.CharField(default="별앤클래식", max_length=100)),
                ("navbar_logo", models.ImageField(blank=True, null=True, upload_to="brand/")),
                ("masthead_hero_image", models.ImageField(blank=True, null=True, upload_to="brand/")),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "verbose_name": "사이트 브랜딩 설정",
                "verbose_name_plural": "사이트 브랜딩 설정",
            },
        ),
    ]
