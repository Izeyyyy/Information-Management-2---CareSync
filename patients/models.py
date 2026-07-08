from django.db import models
from staff.models import ClinicStaff

class Patient(models.Model):

    GENDER_CHOICES = [
        ("male", "Male"),
        ("female", "Female"),
        ("other", "Other"),
    ]

    first_name = models.CharField(
        max_length=150
    )

    middle_name = models.CharField(
        max_length=150,
        blank=True
    )

    last_name = models.CharField(
        max_length=150
    )

    birth_date = models.DateField()

    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES
    )

    contact_number = models.CharField(
        max_length=20
    )

    address = models.TextField()

    created_by_staff = models.ForeignKey(
        ClinicStaff,
        on_delete=models.SET_NULL,
        null=True,
        related_name="registered_patients"
    )

    date_registered = models.DateField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
