from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            "full_name",
            "email",
            "phone",
            "address_line1",
            "address_line2",
            "city",
            "county",
            "postcode",
            "country",
        ]
        widgets = {
            "full_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Your full name", "autocomplete": "name"}),
            "email": forms.EmailInput(attrs={"class": "form-control", "placeholder": "you@example.com", "autocomplete": "email"}),
            "phone": forms.TextInput(attrs={"class": "form-control", "placeholder": "+353 86 123 4567", "autocomplete": "tel"}),
            "address_line1": forms.TextInput(attrs={"class": "form-control", "placeholder": "Address line 1", "autocomplete": "address-line1"}),
            "address_line2": forms.TextInput(attrs={"class": "form-control", "placeholder": "Address line 2 (optional)", "autocomplete": "address-line2"}),
            "city": forms.TextInput(attrs={"class": "form-control", "placeholder": "City/Town", "autocomplete": "address-level2"}),
            "county": forms.TextInput(attrs={"class": "form-control", "placeholder": "County", "autocomplete": "address-level1"}),
            "postcode": forms.TextInput(attrs={"class": "form-control", "placeholder": "Eircode/Postcode", "autocomplete": "postal-code"}),
            "country": forms.TextInput(attrs={"class": "form-control", "placeholder": "Country", "autocomplete": "country-name"}),
        }

    def clean_email(self):
        email = (self.cleaned_data.get("email") or "").strip().lower()
        if not email:
            raise forms.ValidationError("Email is required.")
        qs = User.objects.filter(email__iexact=email)
        if self.instance and self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("That email is already in use.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"].lower()
        if commit:
            user.save()
        return user
