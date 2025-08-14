from django import forms
from django.contrib.auth import get_user_model
from .models import Message

User = get_user_model()

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['recipient', 'subject', 'body']
        widgets = {
            'recipient': forms.Select(attrs={'class': 'form-control'}),
            'subject': forms.TextInput(attrs={'class': 'form-control'}),
            'body': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

    def __init__(self, *args, user=None, **kwargs):
        """
        Filter recipient choices based on the sender:
        - Admins can message anyone.
        - Non-admins can only message admins (staff or superusers).
        """
        super().__init__(*args, **kwargs)

        if user is None:
            allowed = User.objects.none()
        elif user.is_staff or user.is_superuser:
            allowed = User.objects.all().order_by('email')
        else:
            allowed = User.objects.filter(is_staff=True).union(
                User.objects.filter(is_superuser=True)
            ).order_by('email')

        self.fields['recipient'].queryset = allowed

        # If non-admin and there is exactly one admin, preselect it
        if not (user and (user.is_staff or user.is_superuser)) and allowed.count() == 1:
            self.fields['recipient'].initial = allowed.first().pk
