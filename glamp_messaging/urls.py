from django.urls import path
from . import views

app_name = "glamp_messaging"

urlpatterns = [
    path("", views.inbox, name="inbox"),
    path("message/<int:pk>/", views.view_message, name="view_message"),
    path("send/", views.send_message, name="send_message"),
    path("delete/<int:pk>/", views.delete_message, name="delete_message"),
    path("archive/<int:pk>/", views.archive_message, name="archive_message"),
    path("unarchive/<int:pk>/", views.unarchive_message, name="unarchive_message"),
    path("reply/<int:pk>/", views.reply_message, name="reply_message"),
]
