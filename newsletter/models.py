from django.utils import timezone

from django.core.exceptions import ValidationError
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
    recipients = models.ManyToManyField(
        "Subscriber", verbose_name="Получатели", blank=True
    )

    def __str__(self):
        return f"Рассылка № {self.id} (старт: {self.start_time})"

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"

    def update_status(self):
        """Динамическое вычисление и сохранение статуса."""
        now = timezone.now()
        new_status = self.status

        if now < self.start_time:
            new_status = "created"
        elif self.start_time <= now <= self.end_time:
            new_status = "started"
        elif now > self.end_time:
            new_status = "completed"

        if self.status != new_status:
            self.status = new_status
            self.save(update_fields=["status"])

    def clean(self):
        """Валидация полей"""
        if not self.pk and self.start_time < timezone.now():
            raise ValidationError(
                {"start_time": "Время начала не может быть в прошлом."}
            )

        if self.start_time >= self.end_time:
            raise ValidationError(
                "Время начала должно быть строго меньше времени окончания."
            )

    def __str__(self):
        return f"Рассылка № {self.id} (старт: {self.start_time})"


class MailingAttempt(models.Model):
    STATUS_SUCCESS = "Успешно"
    STATUS_FAILURE = "Не успешно"

    STATUS_CHOICES = [
        (STATUS_SUCCESS, "Успешно"),
        (STATUS_FAILURE, "Не успешно"),
    ]

    mailing = models.ForeignKey(
        "Mailing",
        on_delete=models.CASCADE,
        related_name="attempts",
        verbose_name="Рассылка",
    )
    attempt_time = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата и время попытки"
    )

    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, verbose_name="Статус"
    )
    server_response = models.TextField(
        blank=True, null=True, verbose_name="Ответ сервера"
    )

    class Meta:
        verbose_name = "Попытка рассылки"
        verbose_name_plural = "Попытки рассылок"
        ordering = ("-attempt_time",)  # Сначала новые

    def __str__(self):
        return f"Попытка {self.id} для {self.mailing} ({self.get_status_display()})"
