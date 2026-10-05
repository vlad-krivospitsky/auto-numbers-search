from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ["username", "email", "is_staff", "is_active", "date_joined"]
    list_filter = ["is_staff", "is_active"]
    actions = ["make_admin_action", "revoke_admin_action"]

    @admin.action(description="Надати права адміністратора")
    def make_admin_action(self, request, queryset):
        queryset.filter(is_superuser=False).update(is_staff=True)

    @admin.action(description="Скасувати права адміністратора")
    def revoke_admin_action(self, request, queryset):
        queryset.filter(is_superuser=False).update(is_staff=False)
