from django import forms
from .models import Vehicle


class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = [
            "license_plate",
            "region",
            "vendor",
            "model",
            "year_from",
            "fuel",
            "engine_volume",
            "color",
            "body_type",
            "registration_date",
        ]
        widgets = {
            "license_plate": forms.TextInput(
                attrs={
                    "class": "form-control text-uppercase font-monospace",
                    "placeholder": "Наприклад: AA1234BB",
                }
            ),
            "region": forms.Select(attrs={"class": "form-select"}),
            "vendor": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Наприклад: Toyota"}
            ),
            "model": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Наприклад: Camry"}
            ),
            "year_from": forms.NumberInput(
                attrs={"class": "form-control", "placeholder": "2020"}
            ),
            "fuel": forms.Select(attrs={"class": "form-select"}),
            "engine_volume": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "0.1",
                    "placeholder": "2.5",
                }
            ),
            "color": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Чорний"}
            ),
            "body_type": forms.Select(attrs={"class": "form-select"}),
            "registration_date": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            )
        }

    def clean_license_plate(self):
        license_plate = self.cleaned_data.get("license_plate", "").strip().upper()
        return license_plate
