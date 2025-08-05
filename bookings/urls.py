from django.urls import path
from . import views

urlpatterns = [
    path('accommodation/<int:pk>/', views.accommodation_detail, name='accommodation_detail'),
    path('booking-success/', views.booking_success, name='booking_success'),
]

