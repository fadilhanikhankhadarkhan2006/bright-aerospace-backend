from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


class Internship(models.Model):
    company = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'company'}
    )

    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=200)
    stipend = models.CharField(max_length=100, blank=True)

    posted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class InternshipApplication(models.Model):
    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'student'}
    )

    internship = models.ForeignKey(
        Internship,
        on_delete=models.CASCADE,
        related_name="applications"
    )

    applied_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student} -> {self.internship}"