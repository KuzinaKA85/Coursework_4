from django.db import models

from config import settings


class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=150, verbose_name="Имя")
    surname = models.CharField(max_length=150, verbose_name="Отчество")
    last_name = models.CharField(max_length=150, verbose_name="Фамилия")
    comment = models.TextField(verbose_name="Комментарий")

    def __str__(self):
        return f"{self.first_name} {self.surname} {self.last_name}"

    class Meta:
        verbose_name = "Получатель"
        verbose_name_plural = "Получатели"
        ordering = ["email", "first_name", "surname", "last_name"]


class Message(models.Model):
    subject_letter = models.CharField(max_length=300, verbose_name="Тема письма")
    body_letter = models.TextField(verbose_name="Тело письма")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.subject_letter

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"
        ordering = [
            "subject_letter",
        ]


class Mailing(models.Model):
    # owner = models.ForeignKey(  # ДОБАВЛЕНО ПОЛЕ
    #     settings.AUTH_USER_MODEL,
    #     on_delete=models.CASCADE,
    #     verbose_name='Владелец'
    # )
    STATUS_CHOICES = [
        ("created", "Создана"),
        ("started", "Запущена"),
        ("completed", "Завершена"),
    ]

    start_time = models.DateTimeField(verbose_name="Время начала")
    end_time = models.DateTimeField(verbose_name="Время окончания")
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="created", verbose_name="Статус"
    )
    message = models.ForeignKey(
        "Message", on_delete=models.CASCADE, verbose_name="Сообщение"
    )
    clients = models.ManyToManyField(
        "Subscriber", verbose_name="Получатели", blank=True
    )

    def __str__(self):
        return f"Рассылка № {self.id} (старт: {self.start_time})"

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"
