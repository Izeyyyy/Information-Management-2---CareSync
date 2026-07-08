from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Profile


class AccountAuthTests(TestCase):
    def registration_data(self, **overrides):
        data = {
            "first_name": "Ava",
            "middle_initial": "M",
            "last_name": "Reyes",
            "email": "ava@example.com",
            "role": "doctor",
            "password": "StrongPass123!",
            "confirm_password": "StrongPass123!",
        }
        data.update(overrides)
        return data

    def test_registration_creates_user_and_profile(self):
        response = self.client.post(reverse("registration"), self.registration_data())

        self.assertRedirects(response, reverse("login"))
        user = User.objects.get(username="ava@example.com")
        self.assertEqual(user.email, "ava@example.com")
        self.assertEqual(user.first_name, "Ava")
        self.assertTrue(user.check_password("StrongPass123!"))
        self.assertEqual(user.profile.role, "doctor")
        self.assertEqual(user.profile.middle_initial, "M")

    def test_registration_blocks_duplicate_email(self):
        User.objects.create_user(username="ava@example.com", email="ava@example.com", password="StrongPass123!")

        response = self.client.post(reverse("registration"), self.registration_data(email="AVA@example.com"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.filter(email__iexact="ava@example.com").count(), 1)
        self.assertContains(response, "An account with this email already exists.")

    def test_registration_blocks_mismatched_passwords(self):
        response = self.client.post(
            reverse("registration"),
            self.registration_data(confirm_password="DifferentPass123!"),
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.exists())
        self.assertContains(response, "Passwords do not match.")

    def test_login_authenticates_registered_user(self):
        User.objects.create_user(username="ava@example.com", email="ava@example.com", password="StrongPass123!")

        response = self.client.post(
            reverse("login"),
            {"email": "ava@example.com", "password": "StrongPass123!"},
        )

        self.assertRedirects(response, reverse("admin_dashboard"))

    def test_login_rejects_invalid_credentials(self):
        User.objects.create_user(username="ava@example.com", email="ava@example.com", password="StrongPass123!")

        response = self.client.post(
            reverse("login"),
            {"email": "ava@example.com", "password": "wrong-password"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Invalid email or password.")

    def test_dashboard_requires_login(self):
        response = self.client.get(reverse("admin_dashboard"))

        self.assertRedirects(response, f"{reverse('login')}?next={reverse('admin_dashboard')}")

    def test_dashboard_uses_custom_template(self):
        user = User.objects.create_user(
            username="ava@example.com",
            email="ava@example.com",
            password="StrongPass123!",
        )
        Profile.objects.create(user=user, role="staff")
        self.client.login(username="ava@example.com", password="StrongPass123!")

        response = self.client.get(reverse("admin_dashboard"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/admin_dashboard.html")
        self.assertContains(response, "Registered Users")

    def test_logout_ends_session(self):
        User.objects.create_user(username="ava@example.com", email="ava@example.com", password="StrongPass123!")
        self.client.login(username="ava@example.com", password="StrongPass123!")

        response = self.client.get(reverse("logout"))

        self.assertRedirects(response, reverse("login"))
        self.assertNotIn("_auth_user_id", self.client.session)

    def test_default_django_admin_route_is_not_exposed(self):
        response = self.client.get("/admin/")

        self.assertEqual(response.status_code, 404)
