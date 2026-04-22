from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("enroll", "0003_add_career_school"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="enrollapplication",
            name="purposes",
        ),
        migrations.AddField(
            model_name="enrollapplication",
            name="awards_history",
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name="enrollapplication",
            name="practice_time",
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name="enrollapplication",
            name="school_grade",
            field=models.CharField(blank=True, max_length=10),
        ),
        migrations.AddField(
            model_name="enrollapplication",
            name="transcript_available",
            field=models.BooleanField(default=False),
        ),
    ]
