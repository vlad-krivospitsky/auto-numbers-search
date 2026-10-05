from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    email = models.EmailField("Email", unique=True)

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ["-date_joined"]

    def __str__(self):
        role = "Administrator" if self.is_staff else "User"
        return f"{self.username} ({role})"

    def make_admin(self):
        self.is_staff = True
        self.save(update_fields=["is_staff"])

    def revoke_admin(self):
        self.is_staff = False
        self.save(update_fields=["is_staff"])
