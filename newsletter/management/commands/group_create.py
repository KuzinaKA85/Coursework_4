from django.contrib.auth.models import Permission, Group
from django.contrib.contenttypes.models import ContentType
from django.core.management import BaseCommand

from newsletter.models import Subscriber, Message, Mailing
from users.models import User


class Command(BaseCommand):
    help = "Создание группы и назначение прав."

    def handle(self, *args, **kwargs):
        group, created = Group.objects.get_or_create(name="Менеджер")
        content_types = {
            "subscriber": ContentType.objects.get_for_model(Subscriber),
            "message": ContentType.objects.get_for_model(Message),
            "mailing": ContentType.objects.get_for_model(Mailing),
            "user": ContentType.objects.get_for_model(User),
        }
        if created:
            # Права на просмотр всех получателей
            view_all_subscribers = Permission.objects.get(
                content_type=content_types["subscriber"],
                codename="can_view_all_subscribers",
            )
            # Права на просмотр всех сообщений
            view_all_messages = Permission.objects.get(
                content_type=content_types["message"], codename="can_view_all_messages"
            )
            # Права на просмотр всех рассылок
            view_all_mailings = Permission.objects.get(
                content_type=content_types["mailing"], codename="can_view_all_mailings"
            )
            # Права на отключение рассылок
            disable_mailing = Permission.objects.get(
                content_type=content_types["mailing"], codename="can_disable_mailing"
            )
            # Права на просмотр пользователей (из users приложения)
            view_user_permission = Permission.objects.get(
                content_type=content_types["user"], codename="view_user"
            )
            # Права на блокировку пользователей
            change_user_permission = Permission.objects.get(
                content_type=content_types["user"], codename="change_user"
            )
            group.permissions.add(
                view_all_subscribers,
                view_all_messages,
                view_all_mailings,
                disable_mailing,
                view_user_permission,
                change_user_permission,
            )
            self.stdout.write(self.style.SUCCESS("Группа создана, права добавлены."))
        else:
            self.stdout.write(self.style.WARNING("Группа уже существует."))
