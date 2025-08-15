from django import forms


class BookingRequestForm(forms.Form):
    accommodation_id = forms.IntegerField(
        required=False,
        widget=forms.HiddenInput()
    )

    start_date = forms.DateField(
        input_formats=["%Y-%m-%d"],
        widget=forms.DateInput(attrs={"class": "form-control", "autocomplete": "off"}),
        required=True,
    )
    end_date = forms.DateField(
        input_formats=["%Y-%m-%d"],
        widget=forms.DateInput(attrs={"class": "form-control", "autocomplete": "off"}),
        required=True,
    )
    guests = forms.IntegerField(
        min_value=1,
        max_value=12,
        initial=2,
        widget=forms.NumberInput(attrs={"class": "form-control"}),
        help_text="How many guests? (1–12)",
    )
    notes = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={"class": "form-control", "rows": 4, "placeholder": "Any special requests?"}),
    )

    def clean(self):
        cleaned = super().clean()
        start, end = cleaned.get("start_date"), cleaned.get("end_date")
        if start and end and end < start:
            self.add_error("end_date", "End date can’t be before start date.")
        return cleaned
