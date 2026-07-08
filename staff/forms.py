from django import models
from django import forms
from django.contrib.auth.models import User
from .models import ClinicStaff


class UserStaffForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})


class ClinicStaffForm(forms.ModelForm):
    class Meta:
        model = ClinicStaff
        fields = ['date_hired', 'schedule']
        widgets = {
            'date_hired': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'schedule': forms.TextInput(attrs={'placeholder': 'e.g., Mon-Fri, 8AM - 5PM', 'class': 'form-control'}),
        }