from django.urls import path

from newsletter.apps import NewsletterConfig
from newsletter.views import (
    SubscriberListView,
    SubscriberCreateView,
    SubscriberDetailView,
    SubscriberUpdateView,
    SubscriberDeleteView,
    MessageListView,
    MessageCreateView,
    MessageDetailView,
    MessageUpdateView,
    MessageDeleteView,
)

app_name = NewsletterConfig.name

urlpatterns = [
    path("subscribers/", SubscriberListView.as_view(), name="subscriber_list"),
    path("subscriber/new/", SubscriberCreateView.as_view(), name="subscriber_form"),
    path(
        "subscriber/<int:pk>/", SubscriberDetailView.as_view(), name="subscriber_detail"
    ),
    path(
        "subscriber/update/<int:pk>/",
        SubscriberUpdateView.as_view(),
        name="subscriber_update",
    ),
    path(
        "subscriber/delete/<int:pk>/",
        SubscriberDeleteView.as_view(),
        name="subscriber_confirm_delete",
    ),
    path("messages/", MessageListView.as_view(), name="message_list"),
    path("message/new/", MessageCreateView.as_view(), name="message_form"),
    path("message/<int:pk>/", MessageDetailView.as_view(), name="message_detail"),
    path(
        "message/update/<int:pk>/", MessageUpdateView.as_view(), name="message_update"
    ),
    path(
        "message/delete/<int:pk>/",
        MessageDeleteView.as_view(),
        name="message_confirm_delete",
    ),
]
