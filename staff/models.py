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

    schedule = models.CharField(
        max_length=255,
        blank=True
    )

    def __str__(self):
        return self.user.get_full_name()
