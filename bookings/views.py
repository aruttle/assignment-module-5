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
    print("Rendering bookings/accommodation_detail.html for:", accommodation.name)
    return render(request, 'bookings/accommodation_detail.html', context)

def booking_success(request):
    return render(request, 'bookings/booking_success.html')

@login_required
def booking_list(request):
    """
    Show only the current user's bookings, newest first.
    """
    user_bookings = (
        Booking.objects.filter(user=request.user)
        .select_related("accommodation")
        .order_by("-check_in")
    )
    return render(request, 'bookings/booking_list.html', {'bookings': user_bookings})

def accommodation_list(request):
    accommodations = Accommodation.objects.all()
    return render(request, 'bookings/accommodation_list.html', {'accommodations': accommodations})

@login_required
def booking_create(request):
    accommodation_id = request.GET.get('accommodation')
    accommodation = None

    if accommodation_id:
        accommodation = get_object_or_404(Accommodation, pk=accommodation_id)

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            if accommodation:
                booking.accommodation = accommodation
            elif form.cleaned_data.get('accommodation'):
                booking.accommodation = form.cleaned_data['accommodation']
            else:
                messages.error(request, "Accommodation is required.")
                return render(request, 'bookings/booking_form.html', {'form': form})
            # Overlap validation
            overlapping = Booking.objects.filter(
                accommodation=booking.accommodation,
                check_in__lt=booking.check_out,
                check_out__gt=booking.check_in
            ).exists()
            if overlapping:
                messages.error(request, "Selected dates are already booked. Please choose different dates.")
                return render(request, 'bookings/booking_form.html', {'form': form})
            booking.save()
            return redirect('bookings:booking_success')
    else:
        form = BookingForm(initial={'accommodation': accommodation})

    return render(request, 'bookings/booking_form.html', {'form': form, 'is_edit': False})

@login_required
def booking_edit(request, pk):
    """
    Edit an existing booking you own.
    """
    booking = get_object_or_404(Booking.objects.select_related("accommodation"), pk=pk, user=request.user)

    if request.method == 'POST':
        form = BookingForm(request.POST, instance=booking)
        if form.is_valid():
            updated = form.save(commit=False)
            acc = getattr(updated, "accommodation", booking.accommodation)

            # Overlap validation excluding this booking
            overlapping = Booking.objects.filter(
                accommodation=acc,
                check_in__lt=updated.check_out,
                check_out__gt=updated.check_in
            ).exclude(pk=booking.pk).exists()

            if overlapping:
                messages.error(request, "Selected dates are already booked. Please choose different dates.")
            else:
                updated.user = request.user  # safety
                updated.accommodation = acc
                updated.save()
                messages.success(request, "Booking updated.")
                return redirect('bookings:booking_list')
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = BookingForm(instance=booking)

    return render(request, 'bookings/booking_form.html', {'form': form, 'is_edit': True, 'booking': booking})

@login_required
def booking_delete(request, pk):
    """
    Delete a booking you own. GET = confirm page, POST = perform delete.
    """
    booking = get_object_or_404(Booking.objects.select_related("accommodation"), pk=pk, user=request.user)

    if request.method == 'POST':
        name = booking.accommodation.name if booking.accommodation else "Booking"
        booking.delete()
        messages.success(request, f'"{name}" booking deleted.')
        return redirect('bookings:booking_list')

    return render(request, 'bookings/confirm_delete.html', {'booking': booking})
