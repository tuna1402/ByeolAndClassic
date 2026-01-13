from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="EnrollApplication",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=50)),
                ("phone", models.CharField(max_length=30)),
                ("birth_date", models.DateField()),
                ("residence", models.CharField(max_length=100)),
                ("purposes", models.JSONField()),
                ("preferred_date", models.DateField()),
                ("message", models.TextField(blank=True)),
                ("is_handled", models.BooleanField(default=False)),
                ("memo", models.TextField(blank=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "ordering": ["-created_at"],
            },
        ),
    ]
