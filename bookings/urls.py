from django.urls import path
from . import views

app_name = "bookings"

urlpatterns = [
    path('', views.booking_list, name='booking_list'),
    path('accommodation/<int:pk>/', views.accommodation_detail, name='accommodation_detail'),
    path('booking-success/', views.booking_success, name='booking_success'),
    path('accommodations/', views.accommodation_list, name='accommodation_list'),
    path('create/', views.booking_create, name='booking_create')
]



