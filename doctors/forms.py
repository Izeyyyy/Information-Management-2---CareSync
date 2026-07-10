from django import forms
from django.contrib.auth.models import User
from .models import Doctor


class UserDoctorForm(forms.ModelForm):

    password = forms.CharField(
        widget=forms.PasswordInput,
        required=False
    )

    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "password",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({"class": "form-control"})


class DoctorProfileForm(forms.ModelForm):

    class Meta:
        model = Doctor
        fields = [
            "license_number",
            "specialization",
            "availability_status",
        ]

        widgets = {
            "license_number": forms.TextInput(
                attrs={"class": "form-control"}
            ),
            "specialization": forms.Select(
                attrs={"class": "form-select"}
            ),
            "availability_status": forms.Select(
                attrs={"class": "form-select"}
            ),
        }


class DoctorRegistrationForm(forms.ModelForm):

    class Meta:
        model = Doctor
        fields = [
            "license_number",
            "specialization",
        ]

        widgets = {
            "license_number": forms.TextInput(
                attrs={"class": "form-control"}
            ),
            "specialization": forms.Select(
                attrs={"class": "form-select"}
            ),
        }