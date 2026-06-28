"""Routage MON COMMIS."""
from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("api.urls")),
    path("", lambda r: JsonResponse({"service": "MON COMMIS", "admin": "/admin/", "api": "/api/demandes/"})),
]
