from django.db import models


class ContactMessage(models.Model):
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=30)
    email = models.EmailField(blank=True)
    message = models.TextField()
    is_handled = models.BooleanField(default=False)
    memo = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.name} ({self.phone})"
