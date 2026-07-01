from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Profile


def login_view(request):
    return render(request, "accounts/login.html")


def register_view(request):

    if request.method == "POST":

        first_name = request.POST.get("first_name")
        middle_initial = request.POST.get("middle_initial")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        role = request.POST.get("role")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        # Required fields
        if not all([first_name, last_name, email, role, password, confirm_password]):
            messages.error(request, "Please fill in all required fields.")
            return render(request, "accounts/registration.html")

        # Password validation
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, "accounts/registration.html")

        # Duplicate email check
        if User.objects.filter(email=email).exists():
            messages.error(request, "An account with this email already exists.")
            return render(request, "accounts/registration.html")

        # Create Django User
        user = User.objects.create_user(
            username=email,          # Email will serve as username
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password
        )

        # Create Profile
        Profile.objects.create(
            user=user,
            middle_initial=middle_initial,
            role=role
        )

        messages.success(request, "Registration successful. You may now log in.")
        return redirect("login")

    return render(request, "accounts/registration.html")