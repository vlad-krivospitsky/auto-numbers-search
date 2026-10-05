from django.contrib import admin
from .models import Region, Vehicle


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ["code", "name"]
    search_fields = ["code", "name"]


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ["license_plate", "vendor", "model", "year_from", "region", "fuel"]
    list_filter = ["fuel", "body_type", "region"]
    search_fields = ["license_plate", "vendor", "model"]
    ordering = ["-created_at"]
