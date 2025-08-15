# core/urls.py
from django.urls import path
from django.views.generic import TemplateView
from . import views  # keeps your existing home view

app_name = "core"

urlpatterns = [
    path("", views.home, name="home"),
    path("gallery/", TemplateView.as_view(template_name="core/gallery.html"), name="gallery"),
]