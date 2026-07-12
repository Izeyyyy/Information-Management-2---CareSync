from django.shortcuts import render

# Create your views here.
from django.contrib.auth.models import User
from accounts.models import Profile
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import ClinicStaff
from .forms import UserStaffForm, ClinicStaffForm, StaffRegistrationForm
from patients.models import Patient
from django.utils import timezone

@login_required
def staff_dashboard_view(request):

    staff = request.user.clinic_staff

    patients = Patient.objects.all()

    context = {
        "staff": staff,

        "patient_count": patients.count(),

        "today_count":
            patients.filter(
                date_registered=timezone.now().date()
            ).count(),

        "recent_patients":
            patients.order_by("-date_registered")[:5],
    }

    return render(
        request,
        "staff/staff_dashboard.html",
        context,
    )

@login_required
def staff_list(request):
    """System Matrix displaying all active administrative and desk personnel."""
    roster = ClinicStaff.objects.select_related('user').all()
    return render(request, 'staff/staff_list.html', {'roster': roster})


@login_required
def staff_create(request):
    """Operational setup view to onboard a new Clinic Staff entity."""
    if request.method == 'POST':
        user_form = UserStaffForm(request.POST)
        staff_form = ClinicStaffForm(request.POST)

        if user_form.is_valid() and staff_form.is_valid():
            # Save the core authentication account first
            new_user = user_form.save(commit=False)
            # Set a default temporary password for new staff
            new_user.set_password('CareSyncStaff2026!')
            new_user.save()

            # Map profile metadata to the newly generated user ID
            staff_profile = staff_form.save(commit=False)
            staff_profile.user = new_user
            staff_profile.save()

            messages.success(request, f"Staff record for {new_user.get_full_name()} initialized successfully.")
            return redirect('staff_list')
    else:
        user_form = UserStaffForm()
        staff_form = ClinicStaffForm()

    return render(request, 'staff/staff_form.html', {
        'user_form': user_form,
        'staff_form': staff_form,
        'title': 'Onboard Clinic Staff Member'
    })

def staff_registration_view(request):

    registration_data = request.session.get("registration_data")

    if not registration_data:
        messages.error(request, "Please complete the first registration step.")
        return redirect("registration")

    if request.method == "POST":

        form = StaffRegistrationForm(request.POST)

        if form.is_valid():

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
                role="staff",
            )

            staff = form.save(commit=False)
            staff.user = user
            staff.save()

            del request.session["registration_data"]

            messages.success(
                request,
                "Registration completed successfully."
            )

            return redirect("login")

    else:

        form = StaffRegistrationForm()

    return render(
        request,
        "staff/staff_registration.html",
        {
            "form": form,
        },
    )