from django.contrib import admin
from .models import Accommodation

@admin.register(Accommodation)
class AccommodationAdmin(admin.ModelAdmin):
    
    fields = ('name', 'description', 'image_landscape', 'image_portrait', 'price_per_night')
    list_display = ('name', 'price_per_night')
