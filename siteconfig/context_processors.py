from .models import get_site_brand_settings


def site_brand(request):
    return {"site_brand": get_site_brand_settings()}
