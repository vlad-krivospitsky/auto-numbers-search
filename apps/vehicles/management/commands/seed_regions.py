from django.core.management.base import BaseCommand
from apps.vehicles.models import Region

REGIONS_DATA = [
    {"code": "АА, КА, ТА, ТТ", "name": "м. Київ"},
    {"code": "АК, КК", "name": "АР Крим"},
    {"code": "АВ, КВ", "name": "Вінницька область"},
    {"code": "АС, КС", "name": "Волинська область"},
    {"code": "АЕ, КЕ", "name": "Дніпропетровська область"},
    {"code": "АН, КН", "name": "Донецька область"},
    {"code": "АМ, КМ", "name": "Житомирська область"},
    {"code": "АО, КО", "name": "Закарпатська область"},
    {"code": "АР, КР", "name": "Запорізька область"},
    {"code": "АТ, КТ", "name": "Івано-Франківська область"},
    {"code": "AI, KI, ТІ", "name": "Київська область"},
    {"code": "ВА, НА", "name": "Кіровоградська область"},
    {"code": "ВВ, НВ", "name": "Луганська область"},
    {"code": "ВС, НС", "name": "Львівська область"},
    {"code": "ВЕ, НЕ", "name": "Миколаївська область"},
    {"code": "ВН, НН", "name": "Одеська область"},
    {"code": "ВІ, НІ", "name": "Полтавська область"},
    {"code": "ВК, НК", "name": "Рівненська область"},
    {"code": "ВМ, НМ", "name": "Сумська область"},
    {"code": "ВО, HO", "name": "Тернопільська область"},
    {"code": "AX, KX", "name": "Харківська область"},
    {"code": "СА, IA", "name": "Херсонська область"},
    {"code": "СВ, IB", "name": "Хмельницька область"},
    {"code": "СЕ, IE", "name": "Черкаська область"},
    {"code": "СН, IH", "name": "Чернівецька область (та м. Севастополь)"},
    {"code": "СХ, IX", "name": "Чернігівська область"},
]


class Command(BaseCommand):
    help = "Populates SQLite database with Ukrainian regions."

    def handle(self, *args, **options):
        created_count = 0
        for item in REGIONS_DATA:
            region, created = Region.objects.get_or_create(
                code=item["code"], defaults={"name": item["name"]}
            )
            if created:
                created_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Успішно імпортовано {created_count} регіонів у SQLite!"
            )
        )
