from django.contrib import admin

from newsletter.models import Subscriber


@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ("id", "email", "first_name", "surname", "last_name", "comment")
    list_filter = ("email", "first_name", "surname", "last_name")
    search_fields = ("email", "last_name")
