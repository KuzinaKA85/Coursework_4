from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from newsletter.models import Subscriber


class SubscriberListView(ListView):
    model = Subscriber
    template_name = "newsletter/subscriber_list.html"
    context_object_name = "subscriber"


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
    template_name = "subscriber_confirm_delete.html"
    success_url = reverse_lazy("newsletter:subscriber_list")
