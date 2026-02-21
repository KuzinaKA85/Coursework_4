from django.db import models


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
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.subject_letter

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"
        ordering = [
            "subject_letter",
        ]
