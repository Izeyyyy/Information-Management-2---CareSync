from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .forms import LoginForm, RegistrationForm
from .models import Profile


def login_view(request):
    if request.user.is_authenticated:
        return redirect("admin_dashboard")

    if request.method == "POST":
        form = LoginForm(request, data=request.POST)

        if form.is_valid():
            login(request, form.user)
            return redirect("admin_dashboard")

        messages.error(request, "Invalid email or password.")

    return render(request, "accounts/login.html")


def register_view(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)

        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data["email"],
                first_name=form.cleaned_data["first_name"].strip(),
                last_name=form.cleaned_data["last_name"].strip(),
                email=form.cleaned_data["email"],
                password=form.cleaned_data["password"],
            )

            Profile.objects.create(
                user=user,
                middle_initial=form.cleaned_data["middle_initial"].strip().upper(),
                role=form.cleaned_data["role"],
            )

            messages.success(request, "Registration successful. You may now log in.")
            return redirect("login")

        for errors in form.errors.values():
            for error in errors:
                messages.error(request, error)

    return render(request, "accounts/registration.html")


@login_required
def admin_dashboard_view(request):
    users = User.objects.select_related("profile").order_by("last_name", "first_name")

    context = {
        "total_users": users.count(),
        "doctor_count": Profile.objects.filter(role="doctor").count(),
        "staff_count": Profile.objects.filter(role="staff").count(),
        "users": users,
    }

    return render(request, "accounts/admin_dashboard.html", context)


def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect("login")
