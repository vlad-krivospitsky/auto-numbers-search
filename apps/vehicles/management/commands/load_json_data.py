import json
import os
from datetime import datetime
from django.conf import settings
from django.core.management.base import BaseCommand
from apps.vehicles.models import Region, Vehicle


class Command(BaseCommand):
    help = "Imports vehicles from db.json located in the project root"

    BODY_MAPPING = {
        "ХЕТЧБЕК": Vehicle.BodyType.HATCHBACK,
        "СЕДАН": Vehicle.BodyType.SEDAN,
        "УНІВЕРСАЛ": Vehicle.BodyType.WAGON,
        "ВНЕДОРОЖНИК": Vehicle.BodyType.SUV,
        "КРОСОВЕР": Vehicle.BodyType.SUV,
        "КУПЕ": Vehicle.BodyType.COUPE,
        "МІНІВЕН": Vehicle.BodyType.MINIVAN,
    }

    FUEL_MAPPING = {
        "БЕНЗИН": Vehicle.FuelType.PETROL,
        "ДИЗЕЛЬ": Vehicle.FuelType.DIESEL,
        "ЕЛЕКТРО": Vehicle.FuelType.ELECTRIC,
        "ГІБРИД": Vehicle.FuelType.HYBRID,
        "ГАЗ": Vehicle.FuelType.LPG,
        "ГАЗ/БЕНЗИН": Vehicle.FuelType.LPG,
    }

    def handle(self, *args, **options):
        json_path = os.path.join(settings.BASE_DIR, "db.json")

        if not os.path.exists(json_path):
            self.stdout.write(
                self.style.ERROR(f"Файл не знайдено за шляхом: {json_path}")
            )
            return

        with open(json_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        created_count = 0
        skipped_count = 0

        # Загружаем все регионы один раз и строим словарь префикс → регион для O(1) поиска
        all_regions = list(Region.objects.all())
        fallback_region = all_regions[0] if all_regions else None
        prefix_to_region: dict = {}
        for region in all_regions:
            for code in region.code.split(","):
                prefix_to_region[code.strip().upper()] = region

        for item in data:
            license_plate = item.get("N_REG_NEW", "").strip().upper()
            if not license_plate:
                continue

            prefix = license_plate[:2].upper()
            target_region = prefix_to_region.get(prefix, fallback_region)

            d_reg_str = item.get("D_REG")
            registration_date = datetime.now().date()
            if d_reg_str:
                try:
                    registration_date = datetime.strptime(d_reg_str, "%d.%m.%y").date()
                except ValueError:
                    pass

            power_raw = item.get("POWER_KWT")
            power_kwt = float(power_raw) if power_raw else None

            body_raw = item.get("BODY", "").strip().upper()
            body_type = self.BODY_MAPPING.get(body_raw, Vehicle.BodyType.SEDAN)

            fuel_raw = item.get("FUEL", "").strip().upper()
            fuel = self.FUEL_MAPPING.get(fuel_raw, Vehicle.FuelType.PETROL)

            vehicle, created = Vehicle.objects.get_or_create(
                license_plate=license_plate,
                defaults={
                    "region": target_region,
                    "vendor": item.get("BRAND", "UNKNOWN").strip().title(),
                    "model": item.get("MODEL", "UNKNOWN").strip(),
                    "year_from": int(item.get("MAKE_YEAR", 2000)),
                    "fuel": fuel,
                    "engine_volume": None,
                    "color": item.get("COLOR", "НЕВІДОМИЙ").strip().capitalize(),
                    "body_type": body_type,
                    "registration_date": registration_date,
                },
            )

            if created:
                created_count += 1
            else:
                skipped_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Імпорт завершено! Додано: {created_count}, Пропущено: {skipped_count}"
            )
        )
