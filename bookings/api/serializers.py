from rest_framework import serializers
from bookings.models import Accommodation, Booking


class AccommodationSerializer(serializers.ModelSerializer):
    image_landscape_url = serializers.SerializerMethodField()
    image_portrait_url = serializers.SerializerMethodField()

    class Meta:
        model = Accommodation
        fields = [
            "id",
            "name",
            "description",
            "price_per_night",
            "image_landscape_url",
            "image_portrait_url",
        ]

    def get_image_landscape_url(self, obj):
        return obj.image_landscape.url if obj.image_landscape else None

    def get_image_portrait_url(self, obj):
        return obj.image_portrait.url if obj.image_portrait else None


class BookingSerializer(serializers.ModelSerializer):
    accommodation_name = serializers.ReadOnlyField(source="accommodation.name")

    class Meta:
        model = Booking
        fields = [
            "id",
            "accommodation",
            "accommodation_name",
            "check_in",
            "check_out",
            "created_at",
        ]
        read_only_fields = ["created_at"]

    def validate(self, attrs):
        """
        Optional: basic overlap check (server-side) to prevent double-booking
        of the same accommodation.
        """
        accommodation = attrs.get("accommodation")
        check_in = attrs.get("check_in")
        check_out = attrs.get("check_out")

        if check_in and check_out and check_in >= check_out:
            raise serializers.ValidationError("check_out must be after check_in.")

        if accommodation and check_in and check_out:
            qs = (
                Booking.objects
                .filter(accommodation=accommodation)
                .filter(check_in__lt=check_out, check_out__gt=check_in)
            )
            # If updating an existing booking, exclude itself
            if self.instance:
                qs = qs.exclude(pk=self.instance.pk)

            if qs.exists():
                raise serializers.ValidationError("These dates are already booked.")

        return attrs
