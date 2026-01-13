from django.db import migrations


def seed_categories(apps, schema_editor):
    Category = apps.get_model("news", "Category")
    categories = [
        {"code": "notice", "name": "공지사항"},
        {"code": "contest", "name": "콩쿨정보"},
        {"code": "admission", "name": "입시정보"},
    ]
    for category in categories:
        Category.objects.get_or_create(code=category["code"], defaults={"name": category["name"]})


class Migration(migrations.Migration):

    dependencies = [
        ("news", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(seed_categories, migrations.RunPython.noop),
    ]
