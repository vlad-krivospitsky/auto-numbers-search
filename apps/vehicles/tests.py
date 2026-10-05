from datetime import date
from django.test import TestCase
from django.urls import reverse
from apps.accounts.models import User
from apps.vehicles.models import Region, Vehicle


class VehicleAdminCRUDTests(TestCase):
    def setUp(self):
        self.region = Region.objects.create(code="AA", name="м. Київ")

        self.admin_user = User.objects.create_user(
            username="adminuser",
            email="admin@example.com",
            password="password123",
            is_staff=True,
        )

        self.regular_user = User.objects.create_user(
            username="regularuser",
            email="user@example.com",
            password="password123",
            is_staff=False,
        )

        self.vehicle = Vehicle.objects.create(
            license_plate="AA1111AA",
            region=self.region,
            vendor="Toyota",
            model="Camry",
            year_from=2020,
            fuel=Vehicle.FuelType.PETROL,
            color="Чорний",
            body_type=Vehicle.BodyType.SEDAN,
            registration_date=date(2021, 5, 10),
        )

    def test_admin_can_access_create_page(self):
        self.client.login(username="adminuser", password="password123")
        response = self.client.get(reverse("vehicles:create"))
        self.assertEqual(response.status_code, 200)

    def test_admin_can_create_vehicle(self):
        self.client.login(username="adminuser", password="password123")
        data = {
            "license_plate": "KA7777BP",
            "region": self.region.id,
            "vendor": "BMW",
            "model": "X5",
            "year_from": 2022,
            "fuel": Vehicle.FuelType.DIESEL,
            "engine_volume": 3.0,
            "color": "Білий",
            "body_type": Vehicle.BodyType.SUV,
            "registration_date": "2022-01-15",
        }
        response = self.client.post(reverse("vehicles:create"), data)
        new_vehicle = Vehicle.objects.filter(license_plate="KA7777BP").first()
        self.assertIsNotNone(new_vehicle)
        self.assertRedirects(response, reverse("vehicles:detail", kwargs={"pk": new_vehicle.pk}))

    def test_admin_can_access_update_page(self):
        self.client.login(username="adminuser", password="password123")
        response = self.client.get(reverse("vehicles:update", kwargs={"pk": self.vehicle.pk}))
        self.assertEqual(response.status_code, 200)

    def test_admin_can_update_vehicle(self):
        self.client.login(username="adminuser", password="password123")
        data = {
            "license_plate": "AA1111AA",
            "region": self.region.id,
            "vendor": "Toyota",
            "model": "Camry Hybrid",
            "year_from": 2021,
            "fuel": Vehicle.FuelType.HYBRID,
            "color": "Сріблястий",
            "body_type": Vehicle.BodyType.SEDAN,
            "registration_date": "2021-05-10",
        }
        response = self.client.post(reverse("vehicles:update", kwargs={"pk": self.vehicle.pk}), data)
        self.assertRedirects(response, reverse("vehicles:detail", kwargs={"pk": self.vehicle.pk}))
        self.vehicle.refresh_from_db()
        self.assertEqual(self.vehicle.model, "Camry Hybrid")
        self.assertEqual(self.vehicle.fuel, Vehicle.FuelType.HYBRID)

    def test_admin_can_delete_vehicle(self):
        self.client.login(username="adminuser", password="password123")
        response = self.client.post(reverse("vehicles:delete", kwargs={"pk": self.vehicle.pk}))
        self.assertRedirects(response, reverse("vehicles:search"))
        self.assertFalse(Vehicle.objects.filter(pk=self.vehicle.pk).exists())

    def test_regular_user_cannot_access_crud(self):
        self.client.login(username="regularuser", password="password123")
        
        res_create = self.client.get(reverse("vehicles:create"))
        self.assertEqual(res_create.status_code, 403)

        res_update = self.client.get(reverse("vehicles:update", kwargs={"pk": self.vehicle.pk}))
        self.assertEqual(res_update.status_code, 403)

        res_delete = self.client.post(reverse("vehicles:delete", kwargs={"pk": self.vehicle.pk}))
        self.assertEqual(res_delete.status_code, 403)

    def test_unauthenticated_user_cannot_access_crud(self):
        res_create = self.client.get(reverse("vehicles:create"))
        self.assertEqual(res_create.status_code, 403)
