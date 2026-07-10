from django.shortcuts import render

# Create your views here.
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction

from .models import Doctor
from .forms import UserDoctorForm, DoctorProfileForm, DoctorRegistrationForm
from accounts.models import Profile



def is_admin(user):
    return user.is_authenticated and user.is_superuser


@login_required
def doctor_dashboard_view(request):
    """
    Temporary doctor dashboard.
    """

    if not hasattr(request.user, "doctor"):
        messages.error(request, "Access denied.")
        return redirect("login")

    doctor = request.user.doctor

    return render(
        request,
        "doctors/doctor_dashboard.html",
        {
            "doctor": doctor,
        },
    )


@user_passes_test(is_admin)
def doctor_list(request):
    doctors = Doctor.objects.select_related("user").all()

    return render(
        request,
        "doctors/doctor_list.html",
        {
            "doctors": doctors,
        },
    )


@user_passes_test(is_admin)
def doctor_create(request):

    if request.method == "POST":

        user_form = UserDoctorForm(request.POST)
        doctor_form = DoctorProfileForm(request.POST)

        if user_form.is_valid() and doctor_form.is_valid():

            user = user_form.save(commit=False)

            password = request.POST.get("password")

            if password:
                user.set_password(password)
            else:
                user.set_password("Doctor123!")

            user.save()

            Profile.objects.create(
                user=user,
                role="doctor",
                middle_initial=""
            )

            doctor = doctor_form.save(commit=False)
            doctor.user = user
            doctor.save()

            messages.success(request, "Doctor created successfully.")
            return redirect("doctor_list")

    else:
        user_form = UserDoctorForm()
        doctor_form = DoctorProfileForm()

    return render(
        request,
        "doctors/doctor_form.html",
        {
            "user_form": user_form,
            "doctor_form": doctor_form,
            "title": "Create Doctor",
        },
    )


@user_passes_test(is_admin)
def doctor_edit(request, pk):

    doctor = get_object_or_404(Doctor, pk=pk)

    if request.method == "POST":

        user_form = UserDoctorForm(request.POST, instance=doctor.user)
        doctor_form = DoctorProfileForm(request.POST, instance=doctor)

        if user_form.is_valid() and doctor_form.is_valid():

            user_form.save()
            doctor_form.save()

            messages.success(request, "Doctor updated successfully.")
            return redirect("doctor_list")

    else:

        user_form = UserDoctorForm(instance=doctor.user)
        doctor_form = DoctorProfileForm(instance=doctor)

    return render(
        request,
        "doctors/doctor_form.html",
        {
            "user_form": user_form,
            "doctor_form": doctor_form,
            "title": "Edit Doctor",
        },
    )


@user_passes_test(is_admin)
def doctor_delete(request, pk):

    doctor = get_object_or_404(Doctor, pk=pk)

    if request.method == "POST":

        doctor.user.delete()

        messages.success(request, "Doctor deleted successfully.")
        return redirect("doctor_list")

    return render(
        request,
        "doctors/doctor_confirm_delete.html",
        {
            "doctor": doctor,
        },
    )

def doctor_registration_view(request):

    registration_data = request.session.get("registration_data")

    if not registration_data:
        messages.error(request, "Please complete the first registration step.")
        return redirect("registration")

    if request.method == "POST":

        form = DoctorRegistrationForm(request.POST)

        if form.is_valid():
            with transaction.atomic():
                user = User.objects.create_user(
                    username=registration_data["email"],
                    email=registration_data["email"],
                    first_name=registration_data["first_name"],
                    last_name=registration_data["last_name"],
                    password=registration_data["password"],
                )

                Profile.objects.create(
                    user=user,
                    middle_initial=registration_data["middle_initial"],
                    role="doctor",
                )

                doctor = form.save(commit=False)
                doctor.user = user
                doctor.save()

            del request.session["registration_data"]

            messages.success(
                request,
                "Registration completed successfully."
            )

            return redirect("login")

    else:

        form = DoctorRegistrationForm()

    return render(
        request,
        "doctors/doctor_registration.html",
        {
            "form": form,
        },
    )