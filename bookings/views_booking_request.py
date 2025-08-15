from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.timezone import localdate

from .forms_request import BookingRequestForm
from glamp_messaging.models import Message
from .models import Accommodation, Booking
import json


@login_required
def booking_request(request):
    User = get_user_model()
    admins = User.objects.filter(is_active=True, is_staff=True)
    if not admins.exists():
        messages.error(request, "No administrators found to receive your request. Please try again later.")
        return redirect("bookings:booking_list")

    # Resolve accommodation 
    acc_id = request.GET.get("accommodation") or request.POST.get("accommodation_id")
    accommodation = None
    booked_ranges_json = "[]"

    if acc_id and str(acc_id).isdigit():
        accommodation = get_object_or_404(Accommodation, pk=int(acc_id))
        # Build disabled ranges from existing bookings for this accommodation
        bookings = Booking.objects.filter(accommodation=accommodation)
        booked_ranges = [
            {"from": b.check_in.strftime("%Y-%m-%d"), "to": b.check_out.strftime("%Y-%m-%d")}
            for b in bookings
        ]
        booked_ranges_json = json.dumps(booked_ranges)

    if request.method == "POST":
        form = BookingRequestForm(request.POST)
        if form.is_valid():
            start = form.cleaned_data["start_date"]
            end = form.cleaned_data["end_date"]
            guests = form.cleaned_data["guests"]
            notes = form.cleaned_data.get("notes") or ""
            acc_id_clean = form.cleaned_data.get("accommodation_id")

            # Compose subject/body
            acc_part = f" • {accommodation.name}" if accommodation else ""
            subject = f"Booking request: {start} → {end} ({guests} guests){acc_part}"

            user = request.user
            full_name = getattr(user, "full_name", "") or user.email
            phone = getattr(user, "phone", "") or "—"

            body_lines = [
                f"From: {full_name} <{user.email}>",
                f"Phone: {phone}",
                "",
            ]
            if accommodation:
                body_lines += [f"Accommodation: {accommodation.name}", ""]
            body_lines += [
                f"Dates: {start} → {end}",
                f"Guests: {guests}",
                "",
                "Notes:",
                notes if notes else "(none)",
            ]
            body = "\n".join(body_lines)

            for admin in admins:
                Message.objects.create(
                    sender=request.user,
                    recipient=admin,
                    subject=subject,
                    body=body,
                )

            messages.success(request, "Thanks! Your booking request was sent to our team.")
            return redirect("glamp_messaging:inbox")
        messages.error(request, "Please fix the errors below.")
    else:
        # Pre-fill 
        initial = {}
        if accommodation:
            initial["accommodation_id"] = accommodation.id
        form = BookingRequestForm(initial=initial)

    return render(
        request,
        "bookings/booking_request.html",
        {
            "form": form,
            "accommodation": accommodation,
            "booked_ranges_json": booked_ranges_json,
            "today_str": localdate().strftime("%Y-%m-%d"),
        },
    )
