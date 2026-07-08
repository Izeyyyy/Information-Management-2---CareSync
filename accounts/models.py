from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):

    ROLE_CHOICES = [
        ('staff', 'Clinic Staff'),
        ('doctor', 'Doctor'),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile"
    )

    middle_initial = models.CharField(max_length=1, blank=True)

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='staff'
    )

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.get_role_display()}"