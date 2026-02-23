from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.views import View
from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from newsletter.forms import MailingForm, SubscriberForm, MessageForm
from newsletter.models import Subscriber, Message, Mailing, MailingAttempt
from newsletter.services import MailingAttemptService


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

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.save()
        return self.object


class MessageUpdateView(UpdateView):
    model = Message
    form_class = MessageForm
    template_name = "newsletter/message_form.html"
    success_url = reverse_lazy("newsletter:message_list")

    def get_success_url(self):
        return reverse("web_app:message_detail", args=[self.kwargs.get("pk")])


class MessageDeleteView(DeleteView):
    model = Message
    template_name = "newsletter/message_confirm_delete.html"
    context_object_name = "message"
    success_url = reverse_lazy("newsletter:message_list")


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
        context["attempts"] = self.object.attempts.all().order_by("-attempt_time")
        return context

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.update_status()
        return obj


class MailingUpdateView(UpdateView):
    model = Mailing
    form_class = MailingForm
    template_name = "newsletter/mailing_update.html"
    success_url = reverse_lazy("newsletter:mailing_list")

    def get_success_url(self):
        return reverse("newsletter:mailing_detail", args=[self.kwargs.get("pk")])


class MailingDeleteView(DeleteView):
    model = Mailing
    template_name = "newsletter/mailing_confirm_delete.html"
    success_url = reverse_lazy("newsletter:mailing_list")


class MailingStartView(View):

    def get(self, request, *args, **kwargs):
        mailing = get_object_or_404(Mailing, pk=kwargs.get("pk"))

        success, message = MailingAttemptService.send_mailing(mailing)

        if success:
            messages.success(request, message)
        else:
            messages.error(request, message)

        return redirect("web_app:mailing_detail", pk=mailing.pk)


class MailingAttemptListView(ListView):
    model = MailingAttempt
    template_name = "newsletter/mailing_attempt_list.html"
    context_object_name = "mailingattempts"
    queryset = MailingAttempt.objects.all()


class MainView(TemplateView):
    template_name = "newsletter/main.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        now = timezone.now()

        # 1. Общее количество всех созданных рассылок
        context["total_mailings"] = Mailing.objects.count()

        # 2. Количество активных рассылок
        # Условие: start_time <= now <= end_time И статус 'started'
        context["active_mailings"] = Mailing.objects.filter(
            start_time__lte=now, end_time__gte=now, status="started"
        ).count()

        # 3. Количество уникальных получателей
        context["unique_recipients"] = Subscriber.objects.distinct().count()

        return context
