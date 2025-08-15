from django.urls import path
from . import views
from .views_booking_request import booking_request  # keep if you added the request flow

app_name = "bookings"

urlpatterns = [
    path("", views.booking_list, name="booking_list"),
    path("accommodation/<int:pk>/", views.accommodation_detail, name="accommodation_detail"),
    path("booking-success/", views.booking_success, name="booking_success"),
    path("accommodations/", views.accommodation_list, name="accommodation_list"),
    path("create/", views.booking_create, name="booking_create"),
    path("edit/<int:pk>/", views.booking_edit, name="booking_edit"),
    path("delete/<int:pk>/", views.booking_delete, name="booking_delete"),
    path("request/", booking_request, name="booking_request"),
]
