from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_放置
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import ClinicStaff
from .forms import UserStaffForm, ClinicStaffForm


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