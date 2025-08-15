from django.conf import settings
from django.db import models


class GlampProject(models.Model):
    PLANNED = "PLANNED"
    IN_PROGRESS = "IN_PROGRESS"
    ON_HOLD = "ON_HOLD"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"

    STATUS_CHOICES = [
        (PLANNED, "Planned"),
        (IN_PROGRESS, "In Progress"),
        (ON_HOLD, "On Hold"),
        (COMPLETED, "Completed"),
        (CANCELLED, "Cancelled"),
    ]

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PLANNED)

    stakeholders = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        related_name="glamp_projects",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-start_date", "-created_at")
        indexes = [
            models.Index(fields=["status"]),
            models.Index(fields=["name"]),
        ]

    def __str__(self):
        return self.name
