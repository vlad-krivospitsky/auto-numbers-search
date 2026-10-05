from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.conf import settings
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.db.models import Q
from .models import Vehicle
from .forms import VehicleForm

LATIN_TO_CYRILLIC = {
    "A": "А", "B": "В", "C": "С", "E": "Е", "H": "Н", "I": "І",
    "K": "К", "M": "М", "O": "О", "P": "Р", "T": "Т", "X": "Х"
}

CYRILLIC_TO_LATIN = {v: k for k, v in LATIN_TO_CYRILLIC.items()}


def normalize_search_query(query_str: str) -> tuple[str, str]:
    query_str = query_str.strip().upper()
    cyr = "".join(LATIN_TO_CYRILLIC.get(ch, ch) for ch in query_str)
    lat = "".join(CYRILLIC_TO_LATIN.get(ch, ch) for ch in query_str)
    return cyr, lat


class StaffRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    raise_exception = True

    def test_func(self) -> bool:
        return self.request.user.is_staff


class VehicleSearchView(LoginRequiredMixin, ListView):
    model = Vehicle
    paginate_by = 20

    def get_template_names(self):
        if self.request.headers.get("HX-Request"):
            return ["vehicles/partials/vehicle_list.html"]
        return ["vehicles/search.html"]

    def get_queryset(self):
        query = self.request.GET.get("q", "").strip()
        if not query:
            return Vehicle.objects.none()

        cyr_query, lat_query = normalize_search_query(query)
        if any(c.isalpha() for c in query):
            return Vehicle.objects.select_related("region").filter(
                Q(license_plate__istartswith=cyr_query) | Q(license_plate__istartswith=lat_query)
            )
        else:
            return Vehicle.objects.select_related("region").filter(
                Q(license_plate__icontains=cyr_query) | Q(license_plate__icontains=lat_query)
            )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["query"] = self.request.GET.get("q", "")
        return context


class VehicleDetailView(LoginRequiredMixin, DetailView):
    model = Vehicle
    template_name = "vehicles/detail.html"
    context_object_name = "vehicle"
    pk_url_kwarg = "pk"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["car_images_api_key"] = settings.CAR_IMAGES_API_KEY
        return context


class VehicleCreateView(StaffRequiredMixin, CreateView):
    model = Vehicle
    form_class = VehicleForm
    template_name = "vehicles/vehicle_form.html"

    def get_success_url(self):
        return reverse_lazy("vehicles:detail", kwargs={"pk": self.object.pk})


class VehicleUpdateView(StaffRequiredMixin, UpdateView):
    model = Vehicle
    form_class = VehicleForm
    template_name = "vehicles/vehicle_form.html"
    pk_url_kwarg = "pk"

    def get_success_url(self):
        return reverse_lazy("vehicles:detail", kwargs={"pk": self.object.pk})


class VehicleDeleteView(StaffRequiredMixin, DeleteView):
    model = Vehicle
    template_name = "vehicles/vehicle_confirm_delete.html"
    pk_url_kwarg = "pk"
    success_url = reverse_lazy("vehicles:search")
