from django.db import models


class Region(models.Model):

    code = models.CharField(
        "Коди регіону",
        max_length=20,
        unique=True,
    )
    name = models.CharField("Назва області / міста", max_length=100)

    class Meta:
        verbose_name = "Регіон"
        verbose_name_plural = "Регіони"
        ordering = ["name"]

    def __str__(self):
        return f"{self.code} — {self.name}"
