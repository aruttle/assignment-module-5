# users/urls.py
from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import register, profile, switch_user, EmailLoginView

app_name = "users"

urlpatterns = [
    path("register/", register, name="register"),
    path("profile/", profile, name="profile"),

    # Login (email-based form; redirects if already authenticated)
    path(
        "login/",
        EmailLoginView.as_view(redirect_authenticated_user=True),
        name="login",
    ),

    # Secure logout (POST from navbar form); send back to home
    path(
        "logout/",
        LogoutView.as_view(next_page="core:home"),
        name="logout",
    ),

    # Quick “switch account” helper: logs out, then take to login
    path("switch/", switch_user, name="switch_user"),
]
