from django.contrib.sitemaps import Sitemap
from django.utils import timezone

from news.models import Post


class PostSitemap(Sitemap):
    def items(self):
        now = timezone.now()
        return Post.objects.filter(is_published=True, published_at__lte=now)

    def lastmod(self, obj):
        return obj.updated_at
