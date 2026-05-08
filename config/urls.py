from xml.sax.saxutils import escape

from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.http import FileResponse, Http404, HttpResponse
from django.urls import path, include
from django.utils import timezone

SITE_BASE_URL = "https://byeolclassica.pythonanywhere.com"

ROBOTS_TXT = f"""User-agent: *
Disallow:

Sitemap: {SITE_BASE_URL}/sitemap.xml
"""

SITEMAP_STATIC_PATHS = [
    "/",
    "/curriculum/",
    "/admission/yejung-piano/",
    "/admission/yego-piano/",
    "/admission/music-college-piano/",
    "/admission/graduate-piano/",
    "/admission/gwangju-piano-admission/",
    "/admission/jeonnam-piano-admission/",
    "/admission/gwangju-jeonnam-piano-admission/",
    "/admission/gwangju-piano-graduate-admission/",
    "/admission/jeonnam-piano-graduate-admission/",
    "/about/greeting/",
    "/about/profile/",
    "/about/awards/",
    "/news/info/",
    "/news/notice/",
    "/enroll/",
    "/contact/",
]


def _absolute_url(path):
    return f"{SITE_BASE_URL}{path}"


def _sitemap_entry(location, lastmod=None):
    lines = ["  <url>", f"    <loc>{escape(location)}</loc>"]
    if lastmod:
        lines.append(f"    <lastmod>{escape(lastmod)}</lastmod>")
    lines.append("  </url>")
    return "\n".join(lines)


def robots_txt(request):
    return HttpResponse(ROBOTS_TXT, content_type="text/plain; charset=utf-8")


def favicon_ico(request):
    favicon_path = settings.BASE_DIR / "static" / "favicon.ico"
    if not favicon_path.exists():
        raise Http404("favicon.ico not found")
    return FileResponse(open(favicon_path, "rb"), content_type="image/x-icon")


def sitemap_xml(request):
    entries = [_sitemap_entry(_absolute_url(path)) for path in SITEMAP_STATIC_PATHS]

    try:
        from news.models import Post

        now = timezone.now()
        posts = (
            Post.objects.filter(is_published=True, published_at__lte=now)
            .select_related("category")
            .only("slug", "updated_at", "category__code")
        )
        for post in posts:
            path = f"/news/{post.category.code}/{post.slug}/"
            entries.append(_sitemap_entry(_absolute_url(path), post.updated_at.date().isoformat()))
    except Exception:
        # Keep the sitemap available even if optional dynamic post data is temporarily unavailable.
        pass

    entries_xml = "\n".join(entries)
    xml = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"{entries_xml}\n"
        "</urlset>\n"
    )
    return HttpResponse(xml, content_type="application/xml; charset=utf-8")


urlpatterns = [
    path("favicon.ico", favicon_ico, name="favicon_ico"),
    path("robots.txt", robots_txt),
    path("admin/", admin.site.urls),
    path("", include("pages.urls")),
    path("news/", include("news.urls")),
    path("contact/", include("contact.urls")),
    path("enroll/", include("enroll.urls")),
    path("sitemap.xml", sitemap_xml, name="sitemap"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
