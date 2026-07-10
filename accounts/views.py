from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404

from .forms import LoginForm, RegistrationForm, UserForm, ProfileForm
from .models import Profile
from staff.models import ClinicStaff
from doctors.models import Doctor


def is_admin(user):
    return user.is_authenticated and user.is_superuser


def login_view(request):
    # Already logged in? Send them to the correct dashboard.
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect("admin_dashboard")

        try:
            role = request.user.profile.role

            if role == "doctor":
                return redirect("doctor_dashboard")
            elif role == "staff":
                return redirect("staff_dashboard")

        except Profile.DoesNotExist:
            logout(request)
            messages.error(request, "No profile found for this account.")
            return redirect("login")

    if request.method == "POST":
        form = LoginForm(request, data=request.POST)

        if form.is_valid():
            user = form.user
            login(request, user)

            # Administrator
            if user.is_superuser:
                return redirect("admin_dashboard")

            try:
                role = user.profile.role

                if role == "doctor":
                    return redirect("doctor_dashboard")

                elif role == "staff":
                    return redirect("staff_dashboard")

                messages.error(request, "Unknown user role.")

            except Profile.DoesNotExist:
                logout(request)
                messages.error(request, "No profile found for this account.")

        else:
            messages.error(request, "Invalid email or password.")

    return render(request, "accounts/login.html")


def register_view(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)

        if form.is_valid():

            request.session["registration_data"] = {
                "first_name": form.cleaned_data["first_name"].strip(),
                "middle_initial": form.cleaned_data["middle_initial"].strip().upper(),
                "last_name": form.cleaned_data["last_name"].strip(),
                "email": form.cleaned_data["email"].lower(),
                "password": form.cleaned_data["password"],
                "role": form.cleaned_data["role"],
            }

            if form.cleaned_data["role"] == "doctor":
                return redirect("doctor_registration")

            return redirect("staff_registration")

        for errors in form.errors.values():
            for error in errors:
                messages.error(request, error)

    else:
        form = RegistrationForm()

    return render(request, "accounts/registration.html", {
        "form": form,
    })


@user_passes_test(is_admin)
def admin_dashboard_view(request):
    users = User.objects.select_related("profile").order_by("last_name", "first_name")

    context = {
        "total_users": users.count(),
        "doctor_count": Profile.objects.filter(role="doctor").count(),
        "staff_count": Profile.objects.filter(role="staff").count(),
        "users": users,
    }

    return render(request, "accounts/admin_dashboard.html", context)


@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect("login")


# --- Custom Admin CRUD Interfaces (Strictly No Django Admin) ---

@user_passes_test(is_admin)
def user_create(request):
    if request.method == "POST":
        user_form = UserForm(request.POST)
        profile_form = ProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data["password"])
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            profile.middle_initial = profile.middle_initial.strip().upper()
            profile.save()

            # Automatically establish the specialized profile entity record
            if profile.role == "staff":
                ClinicStaff.objects.get_or_create(user=user)
            elif profile.role == "doctor":
                Doctor.objects.get_or_create(user=user)

            messages.success(request, f"User '{user.username}' created successfully.")
            # ---> REDIRECTS BACK TO DASHBOARD HUB
            return redirect("admin_dashboard")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        user_form = UserForm()
        profile_form = ProfileForm()

    return render(request, "accounts/user_form.html", {
        "user_form": user_form,
        "profile_form": profile_form,
        "title": "Create New System Account"
    })


@user_passes_test(is_admin)
def user_edit(request, pk):
    user = get_object_or_404(User, pk=pk)
    profile = get_object_or_404(Profile, user=user)

    if request.method == "POST":
        user_form = UserForm(request.POST, instance=user)
        profile_form = ProfileForm(request.POST, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            updated_user = user_form.save(commit=False)
            if user_form.cleaned_data.get("password"):
                updated_user.set_password(user_form.cleaned_data["password"])
            updated_user.save()

            updated_profile = profile_form.save(commit=False)
            updated_profile.middle_initial = updated_profile.middle_initial.strip().upper()
            updated_profile.save()

            if updated_profile.role == "staff":
                ClinicStaff.objects.get_or_create(user=updated_user)
            elif updated_profile.role == "doctor":
                Doctor.objects.get_or_create(user=updated_user)

            messages.success(request, f"User '{user.username}' updated safely.")
            # ---> REDIRECTS BACK TO DASHBOARD HUB
            return redirect("admin_dashboard")
    else:
        user_form = UserForm(instance=user)
        profile_form = ProfileForm(instance=profile)

    return render(request, "accounts/user_form.html", {
        "user_form": user_form,
        "profile_form": profile_form,
        "title": f"Modify Account Details: {user.username}"
    })


@user_passes_test(is_admin)
def user_delete(request, pk):
    user = get_object_or_404(User, pk=pk)

    if user == request.user:
        messages.error(request, "You cannot delete your own administrative session account.")
        # ---> REDIRECTS BACK TO DASHBOARD HUB
        return redirect("admin_dashboard")

    if request.method == "POST":
        username = user.username
        user.delete()
        messages.success(request, f"User account '{username}' has been successfully purged.")
        # ---> REDIRECTS BACK TO DASHBOARD HUB
        return redirect("admin_dashboard")

    return render(request, "accounts/user_confirm_delete.html", {"user": user})