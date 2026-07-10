from django.urls import path
from . import views

urlpatterns = [
    path("dashboard/", views.staff_dashboard_view, name="staff_dashboard"),

    path(
        "registration/",
        views.staff_registration_view,
        name="staff_registration",
    ),
]
