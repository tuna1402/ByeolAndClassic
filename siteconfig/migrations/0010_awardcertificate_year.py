from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("siteconfig", "0009_homefooterhero"),
    ]

    operations = [
        migrations.AddField(
            model_name="awardcertificate",
            name="year",
            field=models.CharField(blank=True, max_length=4),
        ),
    ]
