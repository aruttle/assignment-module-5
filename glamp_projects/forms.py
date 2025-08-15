from django import forms
from django.contrib.auth import get_user_model
from .models import GlampProject

User = get_user_model()


class ProjectForm(forms.ModelForm):
    class Meta:
        model = GlampProject
        fields = ["name", "description", "start_date", "end_date", "status", "stakeholders"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Project name"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 4, "placeholder": "Optional description"}),
            "start_date": forms.DateInput(attrs={"class": "form-control", "autocomplete": "off"}, format="%Y-%m-%d"),
            "end_date": forms.DateInput(attrs={"class": "form-control", "autocomplete": "off"}, format="%Y-%m-%d"),
            "status": forms.Select(attrs={"class": "form-select"}),
            "stakeholders": forms.SelectMultiple(attrs={"class": "form-select"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Order people show label as full_name or email
        self.fields["stakeholders"].queryset = User.objects.order_by("full_name", "email")
        self.fields["stakeholders"].label_from_instance = (
            lambda u: (u.full_name or u.email) if getattr(u, "full_name", None) else u.email
        )

    def clean(self):
        cleaned = super().clean()
        start, end = cleaned.get("start_date"), cleaned.get("end_date")
        if start and end and end < start:
            self.add_error("end_date", "End date cannot be before start date.")
        return cleaned
