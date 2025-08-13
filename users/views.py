from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect

from .forms import CustomUserCreationForm, EmailAuthForm


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


@login_required
def profile(request):
    return render(request, "registration/profile.html")


def switch_user(request):
    """Log out, then send to login so you can sign in as another user."""
    logout(request)
    messages.info(request, "You're logged out. Sign in with another account.")
    return redirect("users:login")


class EmailLoginView(LoginView):
    """Optional: use this to label the login field as Email."""
    template_name = "registration/login.html"
    authentication_form = EmailAuthForm
