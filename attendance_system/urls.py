from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("dashboard.urls")),
    path("accounts/", include("django.contrib.auth.urls")),
    path("api/", include("students.urls")),
    path("api/", include("teachers.urls")),
    path("api/", include("courses.urls")),
    path("api/", include("attendance.urls")),
]