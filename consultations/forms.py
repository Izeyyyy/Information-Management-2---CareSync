from django import forms

from .models import Consultation


class ConsultationForm(forms.ModelForm):

    class Meta:
        model = Consultation

        fields = [
            "chief_complaint",
            "diagnosis",
            "prescribed_medications",
            "treatment_plan",
            "consultation_notes",
        ]

        widgets = {

            "chief_complaint": forms.Textarea(
                attrs={
                    "rows": 3,
                    "class": "form-control",
                    "placeholder": "Enter the patient's chief complaint...",
                }
            ),

            "diagnosis": forms.Textarea(
                attrs={
                    "rows": 3,
                    "class": "form-control",
                    "placeholder": "Enter the diagnosis...",
                }
            ),

            "prescribed_medications": forms.Textarea(
                attrs={
                    "rows": 3,
                    "class": "form-control",
                    "placeholder": "List prescribed medications...",
                }
            ),

            "treatment_plan": forms.Textarea(
                attrs={
                    "rows": 3,
                    "class": "form-control",
                    "placeholder": "Enter the treatment plan...",
                }
            ),

            "consultation_notes": forms.Textarea(
                attrs={
                    "rows": 4,
                    "class": "form-control",
                    "placeholder": "Additional consultation notes (optional)...",
                }
            ),
        }