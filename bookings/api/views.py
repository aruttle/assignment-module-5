from rest_framework import viewsets, permissions
from bookings.models import Accommodation, Booking
from .serializers import AccommodationSerializer, BookingSerializer


class AccommodationViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Public, read-only list/detail for accommodations.
    """
    queryset = Accommodation.objects.all().order_by("name")
    serializer_class = AccommodationSerializer
    permission_classes = [permissions.AllowAny]


class BookingViewSet(viewsets.ModelViewSet):
    """
    Authenticated users can list/create/update their own bookings.
    """
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return (
            Booking.objects
            .select_related("accommodation")
            .filter(user=self.request.user)
            .order_by("-created_at")
        )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
