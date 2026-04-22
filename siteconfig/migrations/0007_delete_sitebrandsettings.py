from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("siteconfig", "0006_sitebrandsettings_hero_mini_image_1_and_more"),
    ]

    operations = [
        migrations.DeleteModel(name="SiteBrandSettings"),
    ]
