from django.urls import path
from . import views

urlpatterns = [

    path("dashboard/", views.doctor_dashboard_view, name="doctor_dashboard"),

    path("directory/", views.doctor_list, name="doctor_list"),

    path("directory/new/", views.doctor_create, name="doctor_create"),

    path("directory/<int:pk>/edit/", views.doctor_edit, name="doctor_edit"),

    path("directory/<int:pk>/delete/", views.doctor_delete, name="doctor_delete"),

    path(
        "registration/",
        views.doctor_registration_view,
        name="doctor_registration",
    ),
]