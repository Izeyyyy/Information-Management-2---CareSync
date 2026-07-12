from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404

from .forms import PatientForm
from .models import Patient


def is_staff(user):
    return (
        user.is_authenticated
        and hasattr(user, "profile")
        and user.profile.role == "staff"
    )


@user_passes_test(is_staff)
def patient_list(request):

    search = request.GET.get("search", "").strip()

    patients = Patient.objects.all()

    if search:

        patients = patients.filter(

            Q(patient_number__icontains=search)
            | Q(first_name__icontains=search)
            | Q(last_name__icontains=search)

        )

    patients = patients.order_by("-date_registered")

    return render(
        request,
        "patients/patient_list.html",
        {
            "patients": patients,
            "search": search,
        },
    )


@user_passes_test(is_staff)
def patient_create(request):

    if not hasattr(request.user, "clinic_staff"):

        messages.error(
            request,
            "Only clinic staff can register patients."
        )

        return redirect("staff_dashboard")

    if request.method == "POST":

        form = PatientForm(request.POST)

        if form.is_valid():

            patient = form.save(commit=False)

            patient.created_by_staff = request.user.clinic_staff

            patient.save()

            messages.success(
                request,
                "Patient registered successfully."
            )

            return redirect(
                "patient_detail",
                pk=patient.pk
            )

    else:

        form = PatientForm()

    return render(
        request,
        "patients/patient_form.html",
        {
            "form": form,
            "title": "Register Patient",
        },
    )


@user_passes_test(is_staff)
def patient_detail(request, pk):

    patient = get_object_or_404(
        Patient,
        pk=pk
    )

    return render(
        request,
        "patients/patient_detail.html",
        {
            "patient": patient,
        },
    )


@user_passes_test(is_staff)
def patient_edit(request, pk):

    patient = get_object_or_404(
        Patient,
        pk=pk
    )

    if request.method == "POST":

        form = PatientForm(
            request.POST,
            instance=patient
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Patient updated successfully."
            )

            return redirect(
                "patient_detail",
                pk=patient.pk
            )

    else:

        form = PatientForm(
            instance=patient
        )

    return render(
        request,
        "patients/patient_form.html",
        {
            "form": form,
            "title": "Edit Patient",
        },
    )


@user_passes_test(is_staff)
def patient_delete(request, pk):

    patient = get_object_or_404(
        Patient,
        pk=pk
    )

    if request.method == "POST":

        patient.delete()

        messages.success(
            request,
            "Patient deleted successfully."
        )

        return redirect(
            "patient_list"
        )

    return render(
        request,
        "patients/patient_confirm_delete.html",
        {
            "patient": patient,
        },
    )