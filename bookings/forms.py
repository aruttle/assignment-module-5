from django import forms
from .models import Booking

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['check_in', 'check_out']
        widgets = {
            'check_in': forms.DateInput(attrs={
                'type': 'text',
                'id': 'check_in',  
                'placeholder': 'Select check-in date'
            }),
            'check_out': forms.DateInput(attrs={
                'type': 'text',
                'id': 'check_out', 
                'placeholder': 'Select check-out date'
            }),
        }
