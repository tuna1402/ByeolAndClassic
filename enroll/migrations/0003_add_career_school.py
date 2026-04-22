from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("enroll", "0002_add_consultation_types_level_test_piece"),
    ]

    operations = [
        migrations.AddField(
            model_name="enrollapplication",
            name="career_school",
            field=models.CharField(default="", max_length=200, blank=True),
            preserve_default=False,
        ),
    ]
