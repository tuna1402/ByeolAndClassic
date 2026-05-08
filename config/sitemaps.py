from django.contrib.sitemaps import Sitemap
from django.utils import timezone
from django.urls import reverse

from news.models import Post
from pages.admission_pages import ADMISSION_PAGE_SLUGS


class StaticViewSitemap(Sitemap):
    priority = 0.8
    changefreq = "weekly"

    def items(self):
        static_pages = ["home", "greeting", "profile", "awards", "curriculum", "academy_video"]
        admission_pages = [("admission_page", {"slug": slug}) for slug in ADMISSION_PAGE_SLUGS]
        return static_pages + admission_pages

    def location(self, item):
        if isinstance(item, tuple):
            url_name, kwargs = item
            return reverse(url_name, kwargs=kwargs)
        return reverse(item)


class PostSitemap(Sitemap):
    priority = 0.6
    changefreq = "weekly"

    def items(self):
        now = timezone.now()
        return Post.objects.filter(
            is_published=True,
            published_at__lte=now,
        ).select_related("category")

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return reverse(
            "news_detail",
            kwargs={
                "category_code": obj.category.code,
                "slug": obj.slug,
            },
        )


sitemaps = {
    "static": StaticViewSitemap,
    "posts": PostSitemap,
}
