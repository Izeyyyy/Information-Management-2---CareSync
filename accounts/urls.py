from django.urls import path
from . import views

urlpatterns = [
    path("", views.login_view, name="home"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("registration/", views.register_view, name="registration"),
    path("dashboard/", views.admin_dashboard_view, name="admin_dashboard"),

    # Custom Admin User Management Interface (Replaces Django Admin)
    path("dashboard/users/create/", views.user_create, name="user_create"),
    path("dashboard/users/<int:pk>/edit/", views.user_edit, name="user_edit"),
    path("dashboard/users/<int:pk>/delete/", views.user_delete, name="user_delete"),
]