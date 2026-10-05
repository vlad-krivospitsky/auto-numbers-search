from django.urls import path
from .views import (
    VehicleSearchView,
    VehicleDetailView,
    VehicleCreateView,
    VehicleUpdateView,
    VehicleDeleteView,
)

app_name = "vehicles"

urlpatterns = [
    path("", VehicleSearchView.as_view(), name="search"),
    path("vehicle/add/", VehicleCreateView.as_view(), name="create"),
    path("vehicle/<int:pk>/", VehicleDetailView.as_view(), name="detail"),
    path("vehicle/<int:pk>/edit/", VehicleUpdateView.as_view(), name="update"),
    path("vehicle/<int:pk>/delete/", VehicleDeleteView.as_view(), name="delete"),
]
