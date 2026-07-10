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

    SPECIALIZATION_CHOICES = [
        ("General Practitioner", "General Practitioner"),
        ("Family Medicine", "Family Medicine"),
        ("Internal Medicine", "Internal Medicine"),
        ("Pediatrics", "Pediatrics"),
        ("Obstetrics and Gynecology", "Obstetrics and Gynecology"),
        ("Cardiology", "Cardiology"),
        ("Dermatology", "Dermatology"),
        ("Neurology", "Neurology"),
        ("Orthopedics", "Orthopedics"),
        ("Ophthalmology", "Ophthalmology"),
        ("ENT", "Ear, Nose and Throat (ENT)"),
        ("Psychiatry", "Psychiatry"),
        ("Radiology", "Radiology"),
        ("Anesthesiology", "Anesthesiology"),
        ("Emergency Medicine", "Emergency Medicine"),
        ("Other", "Other"),
    ]

    specialization = models.CharField(
        max_length=100,
        choices=SPECIALIZATION_CHOICES,
    )

    STATUS_CHOICES = [
        ("Available", "Available"),
        ("Busy", "Busy"),
        ("Off Duty", "Off Duty"),
    ]

    availability_status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Available",
    )

    def __str__(self):
        return self.user.get_full_name()
