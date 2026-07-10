from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import ClinicStaff


@login_required
def staff_dashboard_view(request):
    """
    Temporary Clinic Staff dashboard.
    Will later become the Patient Registration & Consultation Management dashboard.
    """

    try:
        staff = request.user.clinic_staff
    except ClinicStaff.DoesNotExist:
        messages.error(request, "Clinic Staff profile not found.")
        return render(request, "staff/staff_dashboard.html")

    return render(
        request,
        "staff/staff_dashboard.html",
        {
            "staff": staff,
        },
    )