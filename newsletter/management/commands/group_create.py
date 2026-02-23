from django.contrib.auth.models import Permission, Group
from django.core.management import BaseCommand


class Command(BaseCommand):
    help = "Создание группы и назначение прав."

    def handle(self, *args, **kwargs):
        group, created = Group.objects.get_or_create(name="Пользователь")
        if created:
            permission = Permission.objects.get(codename="can_unpublish_product")
            permission_delete = Permission.objects.get(codename="delete_product")
            group.permissions.add(permission, permission_delete)
            self.stdout.write(self.style.SUCCESS("Группа создана, права добавлены."))
        else:
            self.stdout.write(self.style.WARNING("Группа уже существует."))
