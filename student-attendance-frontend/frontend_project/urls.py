from django.contrib import admin
from django.urls import include, path
from frontend.auth_views import CustomLoginView, CustomLogoutView

urlpatterns = [
    path("admin/", admin.site.urls),

    # Custom Authentication
    path(
        "accounts/login/",
        CustomLoginView.as_view(),
        name="login",
    ),

    path(
        "accounts/logout/",
        CustomLogoutView.as_view(),
        name="logout",
    ),

    # Password reset and other auth URLs
    path("accounts/", include("django.contrib.auth.urls")),

    # Frontend
    path("", include("frontend.urls")),
]