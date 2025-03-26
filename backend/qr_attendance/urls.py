from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from attendance.views import home  # ✅ Import the home view

urlpatterns = [
    path("", home, name="home"),  # ✅ Set Home Page
    path("admin/", admin.site.urls),  # Django Admin Panel
    path("api/", include("attendance.urls")),  # Include attendance app URLs
]

# ✅ Ensure media files are served correctly in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
