from django.urls import path
from . import views

app_name = "api"

urlpatterns = [
    path("demandes/", views.demandes, name="demandes"),
]
