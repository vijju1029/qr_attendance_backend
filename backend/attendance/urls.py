from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import home, employee_list, register_employee, mark_attendance  # Import all views

urlpatterns = [
    path('', home, name='home'),  # Home page
    path('employees/', employee_list, name='employee_list'),  # Employee list
    path('register/', register_employee, name='register_employee'),  # Employee registration
    path('mark_attendance/', mark_attendance, name='mark_attendance'),  # Attendance marking
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
