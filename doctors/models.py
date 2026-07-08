from django.db import models

from django.db import models
from django.contrib.auth.models import User


class Doctor(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="doctor"
    )

    license_number = models.CharField(
        max_length=100,
        unique=True
    )

    specialization = models.CharField(
        max_length=100
    )

    availability_status = models.CharField(
        max_length=50,
        default="Available"
    )

    def __str__(self):
        return self.user.get_full_name()
