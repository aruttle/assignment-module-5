from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AccommodationViewSet, BookingViewSet

router = DefaultRouter()
router.register("accommodations", AccommodationViewSet, basename="api-accommodations")
router.register("bookings", BookingViewSet, basename="api-bookings")

urlpatterns = [
    path("", include(router.urls)),
]
