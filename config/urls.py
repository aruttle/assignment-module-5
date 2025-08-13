from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),

    # Core site
    path("", include(("core.urls", "core"), namespace="core")),

    # Apps
    path("bookings/", include(("bookings.urls", "bookings"), namespace="bookings")),
    path("projects/", include(("glamp_projects.urls", "glamp_projects"), namespace="projects")),

    # Messaging — namespace must match app_name in glamp_messaging/urls.py
    path("messages/", include(("glamp_messaging.urls", "glamp_messaging"), namespace="glamp_messaging")),

    # Users
    path("users/", include(("users.urls", "users"), namespace="users")),

    # API
    path("api/", include("bookings.api.urls")),
    path("api-auth/", include("rest_framework.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)