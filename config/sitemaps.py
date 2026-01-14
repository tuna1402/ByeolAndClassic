from django.contrib.sitemaps import Sitemap
from django.db.models import Q
from django.utils import timezone

from news.models import Post


class PostSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.6

    def items(self):
        now = timezone.now()
        published_filter = Q(published_at__isnull=True) | Q(published_at__lte=now)
        return Post.objects.filter(is_published=True).filter(published_filter)

    def lastmod(self, obj):
        return obj.updated_at or obj.published_at or obj.created_at
