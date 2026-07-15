from django.db import models
from django.db.models import PROTECT

from patients.models import Patient
from doctors.models import Doctor


class Consultation(models.Model):

    patient = models.ForeignKey(
        Patient,
        on_delete=PROTECT,
        related_name="consultations"
    )

    doctor = models.ForeignKey(
        Doctor,
        on_delete=PROTECT,
        related_name="consultations"
    )

    consultation_date = models.DateTimeField(
        auto_now_add=True
    )

    chief_complaint = models.TextField()

    diagnosis = models.TextField()

    prescribed_medications = models.TextField(
        blank=True
    )

    treatment_plan = models.TextField()

    consultation_notes = models.TextField(
        blank=True
    )

    class Meta:
        ordering = ["-consultation_date"]

    @property
    def patient_name(self):
        return self.patient.full_name

    def __str__(self):
        return (
            f"{self.patient.patient_number} - "
            f"{self.consultation_date:%Y-%m-%d %H:%M}"
        )