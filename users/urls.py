# users/urls.py
from django.urls import path, reverse_lazy
from django.contrib.auth.views import (
    LogoutView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)
from .views import register, profile, switch_user, EmailLoginView, edit_profile

app_name = "users"

urlpatterns = [
    path("register/", register, name="register"),
    path("profile/", profile, name="profile"),
    path("profile/edit/", edit_profile, name="edit_profile"),

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

    # --- Password reset flow ---
    path(
        "password-reset/",
        PasswordResetView.as_view(
            template_name="registration/password_reset_form.html",
            email_template_name="registration/password_reset_email.txt",
            subject_template_name="registration/password_reset_subject.txt",
            success_url=reverse_lazy("users:password_reset_done"),
        ),
        name="password_reset",
    ),
    path(
        "password-reset/done/",
        PasswordResetDoneView.as_view(
            template_name="registration/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "password-reset/confirm/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(
            template_name="registration/password_reset_confirm.html",
            success_url=reverse_lazy("users:password_reset_complete"),
        ),
        name="password_reset_confirm",
    ),
    path(
        "password-reset/complete/",
        PasswordResetCompleteView.as_view(
            template_name="registration/password_reset_complete.html"
        ),
        name="password_reset_complete"),
]
