from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("api/", include("api.urls", namespace="api")),
    path("api/", include("users.urls", namespace="users")),
    path("admin/", admin.site.urls),
]
