from django.contrib.sitemaps import Sitemap
from django.utils import timezone
from django.urls import reverse

from news.models import Post


class StaticViewSitemap(Sitemap):
    priority = 0.8
    changefreq = "weekly"

    def items(self):
        return ["home", "greeting", "profile", "awards", "curriculum"]

    def location(self, item):
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
