from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("enroll", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="enrollapplication",
            name="consultation_types",
            field=models.JSONField(default=["수강상담"]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="enrollapplication",
            name="level_test_piece",
            field=models.CharField(default="", max_length=200, blank=True),
            preserve_default=False,
        ),
    ]
