from django.contrib.sitemaps import Sitemap
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
        return Post.objects.filter(is_published=True)

    def lastmod(self, obj):
        return obj.updated_at if hasattr(obj, "updated_at") else None
