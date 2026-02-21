from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from newsletter.models import Subscriber, Message


class SubscriberListView(ListView):
    model = Subscriber
    template_name = "newsletter/subscriber_list.html"
    context_object_name = "subscribers"

    def get_queryset(self):
        return Subscriber.objects.all()


class SubscriberCreateView(CreateView):
    model = Subscriber
    template_name = "newsletter/subscriber_form.html"
    fields = [
        "email",
        "first_name",
        "surname",
        "last_name",
        "comment",
    ]
    success_url = reverse_lazy("newsletter:subscriber_list")


class SubscriberDetailView(DetailView):
    model = Subscriber
    template_name = "newsletter/subscriber_detail.html"
    context_object_name = "subscriber"


class SubscriberUpdateView(UpdateView):
    model = Subscriber
    template_name = "newsletter/subscriber_form.html"
    fields = [
        "email",
        "first_name",
        "surname",
        "last_name",
        "comment",
    ]
    success_url = reverse_lazy("newsletter:subscriber_list")


class SubscriberDeleteView(DeleteView):
    model = Subscriber
    template_name = "newsletter/subscriber_confirm_delete.html"
    context_object_name = "subscriber"
    success_url = reverse_lazy("newsletter:subscriber_list")


class MessageListView(ListView):
    model = Message
    template_name = "newsletter/message_list.html"
    context_object_name = "messages"

    def get_queryset(self):
        return Message.objects.all()


class MessageCreateView(CreateView):
    model = Message
    template_name = "newsletter/message_form.html"
    fields = [
        "subject_letter",
        "body_letter",
    ]
    success_url = reverse_lazy("newsletter:message_list")


class MessageDetailView(DetailView):
    model = Message
    template_name = "newsletter/message_detail.html"
    context_object_name = "message"


class MessageUpdateView(UpdateView):
    model = Message
    template_name = "newsletter/message_form.html"
    fields = [
        "subject_letter",
        "body_letter",
    ]
    success_url = reverse_lazy("newsletter:message_list")


class MessageDeleteView(DeleteView):
    model = Message
    template_name = "newsletter/message_confirm_delete.html"
    context_object_name = "message"
    success_url = reverse_lazy("newsletter:message_list")
