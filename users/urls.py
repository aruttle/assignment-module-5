from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'users'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),

    path(
        'login/',
        auth_views.LoginView.as_view(
            template_name='registration/login.html',  
            redirect_authenticated_user=True,
        ),
        name='login',
    ),

    
    path(
        'logout/',
        auth_views.LogoutView.as_view(next_page='core:home'),
        name='logout',
    ),

    
    path('switch/', views.switch_user, name='switch_user'),
]
