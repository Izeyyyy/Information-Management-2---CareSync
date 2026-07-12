from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone

from .models import Patient


class PatientForm(forms.ModelForm):

    class Meta:
        model = Patient

        fields = [
            "first_name",
            "middle_name",
            "last_name",
            "birth_date",
            "gender",
            "contact_number",
            "address",
        ]

        widgets = {

            "first_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "First Name",
                }
            ),

            "middle_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Middle Name (Optional)",
                }
            ),

            "last_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Last Name",
                }
            ),

            "birth_date": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "form-control",
                }
            ),

            "gender": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "contact_number": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "09XXXXXXXXX",
                }
            ),

            "address": forms.Textarea(
                attrs={
                    "rows": 3,
                    "class": "form-control",
                    "placeholder": "Complete Address",
                }
            ),
        }

    def clean_birth_date(self):

        birth_date = self.cleaned_data["birth_date"]

        if birth_date > timezone.now().date():
            raise ValidationError(
                "Birth date cannot be in the future."
            )

        return birth_date

    def clean_contact_number(self):

        number = self.cleaned_data["contact_number"].strip()

        if len(number) < 10:
            raise ValidationError(
                "Enter a valid contact number."
            )

        return number