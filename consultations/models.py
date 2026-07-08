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

    consultation_date = models.DateTimeField()

    chief_complaint = models.TextField()

    diagnosis = models.TextField()

    treatment_plan = models.TextField()

    prescription = models.TextField(
        blank=True
    )

    medical_notes = models.TextField(
        blank=True
    )

    def __str__(self):
        return f"{self.patient} - {self.consultation_date}"