from django.db import models


class Category(models.Model):
    code = models.SlugField(unique=True)
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return f"{self.name} ({self.code})"


class Post(models.Model):
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="posts")
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    content = models.TextField()
    thumbnail = models.ImageField(upload_to="news/thumbnails/", blank=True)
    attachment = models.FileField(upload_to="news/attachments/", blank=True)
    is_published = models.BooleanField(default=False)
    published_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-published_at", "-created_at"]

    def __str__(self):
        return self.title
