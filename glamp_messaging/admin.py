from django.contrib import admin
from .models import Message


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("subject", "sender", "recipient", "sent_at", "read", "archived")
    list_filter = ("read", "archived", "sent_at")
    search_fields = ("subject", "body", "sender__email", "sender__full_name",
                     "recipient__email", "recipient__full_name")
    date_hierarchy = "sent_at"
