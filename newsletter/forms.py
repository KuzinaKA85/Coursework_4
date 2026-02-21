from django import forms

from .mixins import AllFormMixin
from .models import Mailing, Subscriber, Message


class MailingForm(AllFormMixin, forms.ModelForm):
    class Meta:
        model = Mailing
        fields = ["start_time", "end_time", "status", "message"]
        widgets = {
            "start_time": forms.DateTimeInput(
                attrs={"type": "datetime-local", "class": "form-control"}
            ),
            "end_time": forms.DateTimeInput(
                attrs={"type": "datetime-local", "class": "form-control"}
            ),
        }


class SubscriberForm(AllFormMixin, forms.ModelForm):
    class Meta:
        model = Subscriber
        fields = ["email", "first_name", "surname", "last_name", "comment"]


class MessageForm(AllFormMixin, forms.ModelForm):
    class Meta:
        model = Message
        fields = ["subject_letter", "body_letter"]
