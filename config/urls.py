from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("pages.urls")),
    path("news/", include("news.urls")),
    path("contact/", include("contact.urls")),
    path("enroll/", include("enroll.urls")),
]

# 개발 편의: runserver에서 media 서빙
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
