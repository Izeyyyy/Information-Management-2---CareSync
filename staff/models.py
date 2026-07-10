from django.db import models

from django.db import models
from django.contrib.auth.models import User


class ClinicStaff(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="clinic_staff"
    )

    date_hired = models.DateField()

    SCHEDULE_CHOICES = [
        ("Monday-Friday 8AM-5PM", "Monday-Friday 8AM-5PM"),
        ("Monday-Friday 9AM-6PM", "Monday-Friday 9AM-6PM"),
        ("Monday-Saturday 8AM-5PM", "Monday-Saturday 8AM-5PM"),
        ("Monday-Saturday 9AM-6PM", "Monday-Saturday 9AM-6PM"),
        ("Half Day Morning", "Half Day Morning"),
        ("Half Day Afternoon", "Half Day Afternoon"),
        ("Flexible Schedule", "Flexible Schedule"),
    ]

    schedule = models.CharField(
        max_length=255,
        choices=SCHEDULE_CHOICES,
        blank=True
    )

    def __str__(self):
        return self.user.get_full_name()
