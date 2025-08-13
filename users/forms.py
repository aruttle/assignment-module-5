# from django import forms
# from django.contrib.auth.forms import UserCreationForm, UserChangeForm
# from .models import CustomUser

# class CustomUserCreationForm(UserCreationForm):
#     class Meta:
#         model = CustomUser
#         fields = ("email", "full_name")

# class CustomUserChangeForm(UserChangeForm):
#     class Meta:
#         model = CustomUser
#         fields = ("email", "full_name", "is_active", "is_staff")

# users/forms.py

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (
    UserCreationForm,
    UserChangeForm,
    AuthenticationForm,
)

User = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    """Registration form for your CustomUser (email is the username field)."""

    class Meta(UserCreationForm.Meta):
        model = User
        # password1/password2 are provided by UserCreationForm automatically
        fields = ("email", "full_name")


class CustomUserChangeForm(UserChangeForm):
    """Profile edit form (if/when you need it)."""
    class Meta:
        model = User
        fields = ("email", "full_name")


class EmailAuthForm(AuthenticationForm):
    """Login form that shows 'Email' instead of 'Username'."""
    # Keep field name 'username' (Django expects that), but render as an Email field.
    username = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={"autofocus": True}),
    )


