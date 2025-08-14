from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect

from .forms import CustomUserCreationForm, EmailAuthForm  # your existing forms
from .forms_profile import ProfileUpdateForm  # new lightweight profile form


def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created. Please sign in.")
            return redirect("users:login")
        messages.error(request, "Please fix the errors below.")
    else:
        form = CustomUserCreationForm()
    return render(request, "registration/register.html", {"form": form})


def switch_user(request):
    """
    Log out the current user and send them to the login screen to sign in as another user.
    Works with a normal GET link.
    """
    logout(request)  # clears session even if already anonymous
    messages.info(request, "You're logged out. Please sign in as another user.")
    return redirect("users:login")


@login_required
def profile(request):
    return render(request, "registration/profile.html")


@login_required
def edit_profile(request):
    """
    Allow the logged-in user to update full name and email (email is the username).
    """
    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated.")
            return redirect("users:profile")
        messages.error(request, "Please correct the errors below.")
    else:
        form = ProfileUpdateForm(instance=request.user)
    return render(request, "registration/profile_edit.html", {"form": form})


class EmailLoginView(LoginView):
    """
    Uses your EmailAuthForm so the login field matches EMAIL as USERNAME_FIELD.
    """
    template_name = "registration/login.html"
    authentication_form = EmailAuthForm
