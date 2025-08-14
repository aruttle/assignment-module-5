from django import forms
from django.contrib.auth import get_user_model
from django.db.models import Q
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
        super().__init__(*args, **kwargs)

        if user is None:
            allowed = User.objects.none()
        elif user.is_staff or user.is_superuser:
            # Admins can message anyone
            allowed = User.objects.all().order_by('email')
        else:
            # Non-admins can only message admins
            allowed = User.objects.filter(Q(is_staff=True) | Q(is_superuser=True)).distinct().order_by('email')

        self.fields['recipient'].queryset = allowed

        # Preselect if there is exactly one admin for non-admin users
        if not (user and (user.is_staff or user.is_superuser)) and allowed.count() == 1:
            self.fields['recipient'].initial = allowed.first().pk
