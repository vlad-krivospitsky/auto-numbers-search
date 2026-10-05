from django.db import models
from .region import Region


class Vehicle(models.Model):
    class FuelType(models.TextChoices):
        PETROL = "petrol", "Бензин"
        DIESEL = "diesel", "Дизель"
        ELECTRIC = "electric", "Електро"
        HYBRID = "hybrid", "Гібрид"
        LPG = "lpg", "Газ (ГБО)"

    class BodyType(models.TextChoices):
        SEDAN = "sedan", "Седан"
        HATCHBACK = "hatchback", "Хетчбек"
        SUV = "suv", "Позашляховик / Кросовер"
        WAGON = "wagon", "Універсал"
        COUPE = "coupe", "Купе"
        MINIVAN = "minivan", "Мінівен"

    license_plate = models.CharField(
        "Держ. номер",
        max_length=20,
        unique=True,
    )
    region = models.ForeignKey(
        Region, on_delete=models.PROTECT, related_name="vehicles", verbose_name="Регіон"
    )
    vendor = models.CharField("Марка (Vendor)", max_length=50, db_index=True)
    model = models.CharField("Модель", max_length=50)
    year_from = models.PositiveIntegerField("Рік випуску")
    fuel = models.CharField(
        "Тип пального", max_length=20, choices=FuelType.choices, default=FuelType.PETROL
    )
    engine_volume = models.DecimalField(
        "Об'єм двигуна (л)",
        max_digits=3,
        decimal_places=1,
        null=True,
        blank=True,
    )
    color = models.CharField("Колір", max_length=30)
    body_type = models.CharField(
        "Тип кузова", max_length=30, choices=BodyType.choices, default=BodyType.SEDAN
    )
    registration_date = models.DateField("Дата реєстрації")

    created_at = models.DateTimeField("Дата додавання", auto_now_add=True)

    class Meta:
        verbose_name = "Автомобіль"
        verbose_name_plural = "Автомобілі"
        ordering = ["-created_at"]

    def __str__(self):
        return f"[{self.license_plate}] {self.vendor} {self.model} ({self.year_from})"
