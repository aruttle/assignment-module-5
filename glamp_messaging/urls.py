from django.urls import path
from . import views

app_name = "glamp_messaging"

urlpatterns = [
    path("", views.inbox, name="inbox"),
    path("message/<int:message_id>/", views.view_message, name="view_message"),
    path("send/", views.send_message, name="send_message"),
]
