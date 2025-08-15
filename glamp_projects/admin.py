from django.contrib import admin
from .models import GlampProject


@admin.register(GlampProject)
class GlampProjectAdmin(admin.ModelAdmin):
    list_display = ("name", "status", "start_date", "end_date", "created_at")
    list_filter = ("status",)
    search_fields = ("name", "description")
    filter_horizontal = ("stakeholders",)
    ordering = ("-start_date", "-created_at")
