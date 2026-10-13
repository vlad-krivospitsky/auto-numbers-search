from django.contrib.auth.mixins import AccessMixin


class StaffRequiredMixin(AccessMixin):
    """Verify that the current user is authenticated and is a staff member."""

    raise_exception = True

    def has_permission(self) -> bool:
        return bool(self.request.user.is_authenticated and self.request.user.is_staff)

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)
