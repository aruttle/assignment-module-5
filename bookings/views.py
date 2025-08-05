from django.shortcuts import render, get_object_or_404, redirect
from .models import Booking, Accommodation
from .forms import BookingForm

def accommodation_detail(request, pk):
    accommodation = get_object_or_404(Accommodation, pk=pk)
    
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.save()
            return redirect('booking_success')
    else:
        form = BookingForm(initial={'accommodation': accommodation})

    return render(request, 'bookings/accommodation_detail.html', {
        'accommodation': accommodation,
        'form': form
    })

def booking_success(request):
    return render(request, 'bookings/booking_success.html')
