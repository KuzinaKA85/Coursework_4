from django.contrib import admin

from newsletter.models import Subscriber, Message


@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ("id", "email", "first_name", "surname", "last_name", "comment")
    list_filter = ("email", "first_name", "surname", "last_name")
    search_fields = ("email", "last_name")


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("id", "subject_letter", "body_letter")
    list_filter = ("subject_letter",)
    search_fields = ("subject_letter",)
