from django.db import models
from staff.models import ClinicStaff


class Patient(models.Model):

    GENDER_CHOICES = [
        ("male", "Male"),
        ("female", "Female"),
        ("other", "Other"),
    ]

    first_name = models.CharField(max_length=150)
    middle_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150)

    birth_date = models.DateField()

    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES
    )

    contact_number = models.CharField(max_length=20)

    address = models.TextField()

    patient_number = models.CharField(
        max_length=20,
        unique=True,
        editable=False
    )

    created_by_staff = models.ForeignKey(
        ClinicStaff,
        on_delete=models.SET_NULL,
        null=True,
        related_name="registered_patients"
    )

    date_registered = models.DateField(auto_now_add=True)

    @property
    def full_name(self):
        return " ".join(
            part
            for part in [
                self.first_name,
                self.middle_name,
                self.last_name,
            ]
            if part
        )

    def save(self, *args, **kwargs):
        creating = self.pk is None

        super().save(*args, **kwargs)

        if creating and not self.patient_number:
            self.patient_number = f"PT-{self.pk:05d}"
            Patient.objects.filter(pk=self.pk).update(
                patient_number=self.patient_number
            )

    def __str__(self):
        return f"{self.patient_number} - {self.first_name} {self.last_name}"