from django.urls import path
from .views import (
    SignUpView,
    CustomLoginView,
    CustomLogoutView,
    UserManagementView,
    ToggleAdminRoleView,
)

app_name = "accounts"

urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", CustomLogoutView.as_view(), name="logout"),
    path("users/", UserManagementView.as_view(), name="user_list"),
    path(
        "users/<int:user_id>/toggle-admin/",
        ToggleAdminRoleView.as_view(),
        name="toggle_admin",
    ),
]
