from django import forms
from django.contrib.auth import get_user_model
from .models import Message

User = get_user_model()


class MessageForm(forms.ModelForm):
    recipient = forms.ModelChoiceField(
        queryset=User.objects.none(),
        label="Recipient",
        required=True,
    )

    class Meta:
        model = Message
        fields = ["recipient", "subject", "body"]
        widgets = {
            "subject": forms.TextInput(attrs={"placeholder": "Subject"}),
            "body": forms.Textarea(attrs={"rows": 6, "placeholder": "Write your message…"}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)  
        super().__init__(*args, **kwargs)

        # Build the recipient queryset based on who is composing
        if user is not None:
            if user.is_staff:
                qs = User.objects.filter(is_active=True).exclude(pk=user.pk)
            else:
                qs = User.objects.filter(is_active=True, is_staff=True)
        else:
            # Fallback
            qs = User.objects.filter(is_active=True, is_staff=True)

        # Order by name then email
        self.fields["recipient"].queryset = qs.order_by("full_name", "email")

        # Bootstrap classes
        self.fields["recipient"].widget.attrs.update({"class": "form-select"})
        self.fields["subject"].widget.attrs.update({"class": "form-control"})
        self.fields["body"].widget.attrs.update({"class": "form-control"})
