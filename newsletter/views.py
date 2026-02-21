from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from newsletter.forms import MailingForm, SubscriberForm, MessageForm
from newsletter.models import Subscriber, Message, Mailing


class MailingListView(ListView):
    model = Mailing
    template_name = "newsletter/mailing_list.html"
    context_object_name = "mailings"


class MailingCreateView(CreateView):
    model = Mailing
    form_class = MailingForm
    template_name = "newsletter/mailing_form.html"
    success_url = reverse_lazy("newsletter:mailing_list")


class MailingDetailView(DetailView):
    model = Mailing
    template_name = "newsletter/mailing_detail.html"
    context_object_name = "mailing"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Явно получаем получателей и добавляем в контекст
        context["clients_list"] = self.object.clients.all()
        return context


class MailingUpdateView(UpdateView):
    model = Mailing
    form_class = MailingForm
    template_name = "newsletter/mailing_update.html"
    success_url = reverse_lazy("newsletter:mailing_list")


class MailingDeleteView(DeleteView):
    model = Mailing
    template_name = "newsletter/mailing_confirm_delete.html"
    success_url = reverse_lazy("newsletter:mailing_list")


class SubscriberListView(ListView):
    model = Subscriber
    template_name = "newsletter/subscriber_list.html"
    context_object_name = "subscribers"

    def get_queryset(self):
        return Subscriber.objects.all()


class SubscriberCreateView(CreateView):
    model = Subscriber
    form_class = SubscriberForm
    template_name = "newsletter/subscriber_form.html"
    context_object_name = "subscriber"
    success_url = reverse_lazy("newsletter:subscriber_list")


class SubscriberDetailView(DetailView):
    model = Subscriber
    template_name = "newsletter/subscriber_detail.html"
    context_object_name = "subscriber"


class SubscriberUpdateView(UpdateView):
    model = Subscriber
    form_class = SubscriberForm
    template_name = "newsletter/subscriber_form.html"
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
    form_class = MessageForm
    template_name = "newsletter/message_form.html"
    success_url = reverse_lazy("newsletter:message_list")


class MessageDetailView(DetailView):
    model = Message
    template_name = "newsletter/message_detail.html"
    context_object_name = "message"


class MessageUpdateView(UpdateView):
    model = Message
    form_class = MessageForm
    template_name = "newsletter/message_form.html"
    success_url = reverse_lazy("newsletter:message_list")


class MessageDeleteView(DeleteView):
    model = Message
    template_name = "newsletter/message_confirm_delete.html"
    context_object_name = "message"
    success_url = reverse_lazy("newsletter:message_list")
