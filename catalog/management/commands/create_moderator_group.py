from django.contrib.auth.models import Group, Permission
from django.core.management.base import (
    BaseCommand,
    CommandError,
)


class Command(BaseCommand):
    help = "Создаёт группу модераторов продуктов"

    def handle(self, *args, **options):
        group, created = Group.objects.get_or_create(
            name="Модератор продуктов"
        )

        permissions = Permission.objects.filter(
            content_type__app_label="catalog",
            codename__in=[
                "can_unpublish_product",
                "delete_product",
            ],
        )

        if permissions.count() != 2:
            raise CommandError(
                "Не найдены права can_unpublish_product "
                "и delete_product. Сначала выполните миграции."
            )

        group.permissions.set(permissions)

        if created:
            message = "Группа модераторов создана."
        else:
            message = "Права группы модераторов обновлены."

        self.stdout.write(
            self.style.SUCCESS(message)
        )