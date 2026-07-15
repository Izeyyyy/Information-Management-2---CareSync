from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from .models import Consultation
from .forms import ConsultationForm
from patients.models import Patient


def is_doctor(user):
    return (
        user.is_authenticated
        and hasattr(user, "profile")
        and user.profile.role == "doctor"
    )

def is_staff_or_doctor(user):
    return (
        user.is_authenticated
        and hasattr(user, "profile")
        and user.profile.role in ["staff", "doctor"]
    )


@user_passes_test(is_doctor)
def consultation_create(request, patient_pk):

    patient = get_object_or_404(
        Patient,
        pk=patient_pk
    )

    if request.method == "POST":

        form = ConsultationForm(request.POST)

        if form.is_valid():

            consultation = form.save(commit=False)

            consultation.patient = patient
            consultation.doctor = request.user.doctor
            consultation.consultation_date = timezone.now()

            consultation.save()

            messages.success(
                request,
                "Consultation recorded successfully."
            )

            return redirect(
                "patient_detail",
                pk=patient.pk
            )

    else:

        form = ConsultationForm()

    return render(
        request,
        "consultations/consultation_form.html",
        {
            "form": form,
            "patient": patient,
            "title": "New Consultation",
        },
    )


@user_passes_test(is_staff_or_doctor)
def consultation_detail(request, pk):

    consultation = get_object_or_404(
        Consultation.objects.select_related(
            "patient",
            "doctor",
            "doctor__user",
        ),
        pk=pk,
    )

    return render(
        request,
        "consultations/consultation_detail.html",
        {
            "consultation": consultation,
            "patient": consultation.patient,
            "is_staff": request.user.profile.role == "staff",
            "is_doctor": request.user.profile.role == "doctor",
        },
    )


@user_passes_test(is_doctor)
def consultation_edit(request, pk):

    consultation = get_object_or_404(
        Consultation,
        pk=pk
    )

    if request.method == "POST":

        form = ConsultationForm(
            request.POST,
            instance=consultation
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Consultation updated successfully."
            )

            return redirect(
                "consultation_detail",
                pk=consultation.pk
            )

    else:

        form = ConsultationForm(
            instance=consultation
        )

    return render(
        request,
        "consultations/consultation_form.html",
        {
            "form": form,
            "consultation": consultation,
            "patient": consultation.patient,
            "title": "Edit Consultation",
        },
    )


@user_passes_test(is_doctor)
def consultation_delete(request, pk):

    consultation = get_object_or_404(
        Consultation,
        pk=pk
    )

    patient = consultation.patient

    if request.method == "POST":

        consultation.delete()

        messages.success(
            request,
            "Consultation deleted successfully."
        )

        return redirect(
            "patient_detail",
            pk=patient.pk
        )

    return render(
        request,
        "consultations/consultation_confirm_delete.html",
        {
            "consultation": consultation,
        },
    )