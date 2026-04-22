from django.db import models


class EnrollApplication(models.Model):
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=30)
    birth_date = models.DateField()
    residence = models.CharField(max_length=100)
    consultation_types = models.JSONField()
    level_test_piece = models.CharField(max_length=200, blank=True)
    career_school = models.CharField(max_length=200, blank=True)
    awards_history = models.TextField(blank=True)
    practice_time = models.CharField(max_length=50, blank=True)
    school_grade = models.CharField(max_length=10, blank=True)
    transcript_available = models.BooleanField(default=False)
    preferred_date = models.DateField()
    message = models.TextField(blank=True)
    is_handled = models.BooleanField(default=False)
    memo = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.name} ({self.phone})"
