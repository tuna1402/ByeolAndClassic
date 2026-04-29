from django.http import FileResponse
from pathlib import Path
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from .sitemaps import sitemaps

BASE_DIR = Path(__file__).resolve().parents[1]


def robots_txt(request):
    return FileResponse(open(BASE_DIR / "robots.txt", "rb"), content_type="text/plain")


urlpatterns = [
    path("robots.txt", robots_txt),
    path("admin/", admin.site.urls),
    path("", include("pages.urls")),
    path("news/", include("news.urls")),
    path("contact/", include("contact.urls")),
    path("enroll/", include("enroll.urls")),
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="sitemap"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
