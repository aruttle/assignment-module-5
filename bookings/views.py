from django.shortcuts import render, get_object_or_404, redirect
from .models import Accommodation, Booking
from .forms import BookingForm
import json

def accommodation_detail(request, pk):
    accommodation = get_object_or_404(Accommodation, pk=pk)

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user  # Make sure the user is assigned
            booking.accommodation = accommodation  # Assign accommodation to booking
            booking.save()
            return redirect('booking_success')  # Ensure this URL name matches your urls.py
    else:
        form = BookingForm(initial={'accommodation': accommodation})

    # Get all bookings for this accommodation
    bookings = Booking.objects.filter(accommodation=accommodation)

    # Format booked date ranges for JS (flatpickr disables)
    booked_ranges = [
        {
            'start': booking.check_in.strftime('%Y-%m-%d'),
            'end': booking.check_out.strftime('%Y-%m-%d')
        }
        for booking in bookings
    ]

    context = {
        'accommodation': accommodation,
        'form': form,
        'booked_ranges_json': json.dumps(booked_ranges),
    }

    return render(request, 'bookings/accommodation_detail.html', context)


def booking_success(request):
    return render(request, 'bookings/booking_success.html')
