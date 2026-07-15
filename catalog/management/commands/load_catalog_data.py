from django.core.management import call_command
from django.core.management.base import BaseCommand

from catalog.models import Category, Product


class Command(BaseCommand):
    """Загружает категории и продукты из фикстуры."""

    help = "Загрузка категорий и продуктов из фикстуры"

    def handle(self, *args, **options):
        self.stdout.write("Удаление старых данных...")

        Product.objects.all().delete()
        Category.objects.all().delete()

        self.stdout.write("Загрузка данных из фикстуры...")

        call_command("loaddata", "catalog_data.json")

        self.stdout.write(
            self.style.SUCCESS(
                "Категории и продукты успешно загружены."
            )
        )