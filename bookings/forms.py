from django import forms
from .models import Booking

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['accommodation', 'check_in', 'check_out']
        widgets = {
            'check_in': forms.DateInput(attrs={
                'type': 'text',
                'id': 'check_in_date',
                'placeholder': 'Select check-in date'
            }),
            'check_out': forms.DateInput(attrs={
                'type': 'text',
                'id': 'check_out_date',
                'placeholder': 'Select check-out date'
            }),
            'accommodation': forms.HiddenInput()
        }
