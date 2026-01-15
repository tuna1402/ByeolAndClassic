from django.apps import AppConfig


class SiteconfigConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "siteconfig"
    verbose_name = "사이트 브랜딩 설정"
