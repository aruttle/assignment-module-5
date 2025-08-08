from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Accommodation, Booking
from .forms import BookingForm
import json

def accommodation_detail(request, pk):
    accommodation = get_object_or_404(Accommodation, pk=pk)

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            new_check_in = form.cleaned_data['check_in']
            new_check_out = form.cleaned_data['check_out']

            # Check for overlapping bookings
            overlapping = Booking.objects.filter(
                accommodation=accommodation,
                check_in__lt=new_check_out,
                check_out__gt=new_check_in
            ).exists()

            if overlapping:
                messages.error(request, "Selected dates are already booked. Please choose different dates.")
            else:
                booking = form.save(commit=False)
                booking.user = request.user
                booking.accommodation = accommodation
                booking.save()
                return redirect('bookings:booking_success')
    else:
        form = BookingForm(initial={'accommodation': accommodation})

    bookings = Booking.objects.filter(accommodation=accommodation)

    booked_ranges = [
        {
            'from': booking.check_in.strftime('%Y-%m-%d'),
            'to': booking.check_out.strftime('%Y-%m-%d')
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

def booking_list(request):
    return render(request, 'bookings/booking_list.html')

def accommodation_list(request):
    accommodations = Accommodation.objects.all()
    return render(request, 'bookings/accommodation_list.html', {'accommodations': accommodations})

@login_required
def booking_create(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.save()
            return redirect('bookings:booking_success')
    else:
        form = BookingForm()

    return render(request, 'bookings/booking_form.html', {'form': form})
