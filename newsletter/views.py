from multiprocessing.managers import dispatch

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.cache import cache_page
from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from newsletter.forms import MailingForm, SubscriberForm, MessageForm
from newsletter.models import Subscriber, Message, Mailing, MailingAttempt
from newsletter.services import MailingAttemptService


def can_edit_object(user, obj):
    """Может ли пользователь редактировать/удалять объект"""
    return user.is_superuser or obj.owner == user


def can_view_object(user, obj):
    """Может ли пользователь просматривать объект"""
    if user.is_superuser:
        return True
    if user.has_perm("newsletter.can_view_all_subscribers") or user.has_perm(
        "newsletter.can_view_all_mailings"
    ):
        return True
    return obj.owner == user


class SubscriberListView(LoginRequiredMixin, ListView):
    model = Subscriber
    template_name = "newsletter/subscriber_list.html"
    context_object_name = "subscribers"

    def get_queryset(self):
        # Менеджеры и админы видят всех
        if self.request.user.is_superuser or self.request.user.has_perm(
            "newsletter.can_view_all_subscribers"
        ):
            return Subscriber.objects.all()
        # Обычные пользователи видят только своих
        return Subscriber.objects.filter(owner=self.request.user)


class SubscriberCreateView(LoginRequiredMixin, CreateView):
    model = Subscriber
    form_class = SubscriberForm
    template_name = "newsletter/subscriber_form.html"
    context_object_name = "subscriber"
    success_url = reverse_lazy("newsletter:subscriber_list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


@method_decorator(cache_page(60 * 5), name="dispatch")
class SubscriberDetailView(LoginRequiredMixin, DetailView):
    model = Subscriber
    template_name = "newsletter/subscriber_detail.html"
    context_object_name = "subscriber"

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if not can_view_object(self.request.user, obj):
            raise PermissionDenied("У вас нет прав для просмотра этого получателя")
        return obj


class SubscriberUpdateView(LoginRequiredMixin, UpdateView):
    model = Subscriber
    form_class = SubscriberForm
    template_name = "newsletter/subscriber_form.html"
    success_url = reverse_lazy("newsletter:subscriber_list")

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if not can_edit_object(self.request.user, obj):
            raise PermissionDenied("Вы можете редактировать только своих получателей")
        return obj


class SubscriberDeleteView(LoginRequiredMixin, DeleteView):
    model = Subscriber
    template_name = "newsletter/subscriber_confirm_delete.html"
    context_object_name = "subscriber"
    success_url = reverse_lazy("newsletter:subscriber_list")

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if not can_edit_object(self.request.user, obj):
            raise PermissionDenied("Вы можете удалять только своих получателей")
        return obj


class MessageListView(LoginRequiredMixin, ListView):
    model = Message
    template_name = "newsletter/message_list.html"
    context_object_name = "messages"

    def get_queryset(self):
        if self.request.user.is_superuser or self.request.user.has_perm(
            "newsletter.can_view_all_messages"
        ):
            return Message.objects.all()
        return Message.objects.filter(owner=self.request.user)


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    template_name = "newsletter/message_form.html"
    success_url = reverse_lazy("newsletter:message_list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


@method_decorator(cache_page(60 * 5), name="dispatch")
class MessageDetailView(LoginRequiredMixin, DetailView):
    model = Message
    template_name = "newsletter/message_detail.html"
    context_object_name = "message"

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if not can_view_object(self.request.user, obj):
            raise PermissionDenied("У вас нет прав для просмотра этого сообщения")
        return obj

    # def get_object(self, queryset=None):
    #     self.object = super().get_object(queryset)
    #     self.object.save()
    #     return self.object


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    form_class = MessageForm
    template_name = "newsletter/message_form.html"
    success_url = reverse_lazy("newsletter:message_list")

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if not can_edit_object(self.request.user, obj):
            raise PermissionDenied("Вы можете редактировать только свои сообщения")
        return obj

    def get_success_url(self):
        return reverse("web_app:message_detail", args=[self.kwargs.get("pk")])


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    template_name = "newsletter/message_confirm_delete.html"
    context_object_name = "message"
    success_url = reverse_lazy("newsletter:message_list")

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if not can_edit_object(self.request.user, obj):
            raise PermissionDenied("Вы можете удалять только свои сообщения")
        return obj


class MailingListView(LoginRequiredMixin, ListView):
    model = Mailing
    template_name = "newsletter/mailing_list.html"
    context_object_name = "mailings"

    def get_queryset(self):
        if self.request.user.is_superuser or self.request.user.has_perm(
            "newsletter.can_view_all_mailings"
        ):
            return Mailing.objects.all()
        return Mailing.objects.filter(owner=self.request.user)


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    form_class = MailingForm
    template_name = "newsletter/mailing_form.html"
    success_url = reverse_lazy("newsletter:mailing_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Передаем в шаблон списки сообщений и получателей текущего пользователя
        context["messages"] = Message.objects.filter(owner=self.request.user)
        context["subscribers"] = Subscriber.objects.filter(owner=self.request.user)
        return context

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


@method_decorator(cache_page(60 * 5), name="dispatch")
class MailingDetailView(LoginRequiredMixin, DetailView):
    model = Mailing
    template_name = "newsletter/mailing_detail.html"
    context_object_name = "mailing"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["attempts"] = self.object.attempts.all().order_by("-attempt_time")
        return context

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if not can_view_object(self.request.user, obj):
            raise PermissionDenied("У вас нет прав для просмотра этой рассылки")
        obj.update_status()
        return obj


class MailingUpdateView(LoginRequiredMixin, UpdateView):
    model = Mailing
    form_class = MailingForm
    template_name = "newsletter/mailing_update.html"
    success_url = reverse_lazy("newsletter:mailing_list")

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if not can_edit_object(self.request.user, obj):
            raise PermissionDenied("Вы можете редактировать только свои рассылки")
        return obj

    def get_success_url(self):
        return reverse("newsletter:mailing_detail", args=[self.kwargs.get("pk")])


class MailingDeleteView(LoginRequiredMixin, DeleteView):
    model = Mailing
    template_name = "newsletter/mailing_confirm_delete.html"
    success_url = reverse_lazy("newsletter:mailing_list")

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if not can_edit_object(self.request.user, obj):
            raise PermissionDenied("Вы можете удалять только свои рассылки")
        return obj


class MailingDisableView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = "newsletter.can_disable_mailing"

    def post(self, request, pk):
        mailing = get_object_or_404(Mailing, pk=pk)
        mailing.is_active = False
        mailing.save()
        messages.success(request, f'Рассылка "{mailing}" отключена')
        return redirect("newsletter:mailing_detail", pk=pk)


class MailingStartView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        mailing = get_object_or_404(Mailing, pk=kwargs.get("pk"))

        # Проверка: владелец ИЛИ менеджер ИЛИ админ
        is_owner = mailing.owner == request.user
        is_manager = request.user.groups.filter(name="Менеджер").exists()
        is_admin = request.user.is_superuser

        if not (is_owner or is_manager or is_admin):
            raise PermissionDenied("У вас нет прав для запуска этой рассылки")

        success, message = MailingAttemptService.send_mailing(mailing)

        if success:
            messages.success(request, message)
        else:
            messages.error(request, message)

        return redirect("newsletter:mailing_detail", pk=mailing.pk)


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

        context["total_mailings"] = Mailing.objects.count()

        # Условие: start_time <= now <= end_time И статус 'started'
        context["active_mailings"] = Mailing.objects.filter(
            start_time__lte=now, end_time__gte=now, status="started"
        ).count()

        context["unique_recipients"] = Subscriber.objects.distinct().count()

        return context
