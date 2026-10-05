from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView, ListView, View
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm
from .models import User


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("accounts:login")
    template_name = "accounts/signup.html"


class CustomLoginView(LoginView):
    template_name = "accounts/login.html"


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy("vehicles:search")


class UserManagementView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = User
    template_name = "accounts/user_list.html"
    context_object_name = "users"
    raise_exception = True

    def test_func(self) -> bool:
        return self.request.user.is_staff

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["users_count"] = self.get_queryset().count()
        return context


class ToggleAdminRoleView(LoginRequiredMixin, UserPassesTestMixin, View):
    raise_exception = True

    def test_func(self) -> bool:
        return self.request.user.is_staff

    def post(self, request, user_id: int):
        user_to_change = get_object_or_404(User, pk=user_id)

        if not user_to_change.is_superuser and user_to_change != request.user:
            if user_to_change.is_staff:
                user_to_change.revoke_admin()
            else:
                user_to_change.make_admin()

        return redirect("accounts:user_list")