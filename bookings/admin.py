from django.contrib import admin
from .models import Accommodation, Booking

@admin.register(Accommodation)
class AccommodationAdmin(admin.ModelAdmin):
    fields = ('name', 'description', 'image_landscape', 'image_portrait', 'price_per_night')
    list_display = ('name', 'price_per_night')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'accommodation', 'check_in', 'check_out', 'created_at')
    list_filter = ('accommodation', 'check_in', 'check_out')
    search_fields = ('user__email', 'accommodation__name')
