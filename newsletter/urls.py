from django.urls import path

from newsletter.apps import NewsletterConfig
from newsletter.views import (SubscriberListView, SubscriberCreateView,
                              SubscriberDetailView, SubscriberUpdateView, SubscriberDeleteView)

app_name = NewsletterConfig.name

urlpatterns = [
    path("", SubscriberListView.as_view(), name="subscriber_list"),
    path("subscriber/new/", SubscriberCreateView.as_view(), name="subscriber_form"),
    path("subscriber/<int:pk>/", SubscriberDetailView.as_view(), name="subscriber_detail"),
    path("subscriber/update/<int:pk>/", SubscriberUpdateView.as_view(), name="subscriber_update"),
    path("subscriber/delete/<int:pk>/", SubscriberDeleteView.as_view(), name="subscriber_confirm_delete"),
]