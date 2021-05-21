# -*- coding: utf-8 -*-
from django.urls import path

from . import views

app_name = "stripe"
urlpatterns = [
    path(
        "",
        views.PaymentView.as_view(),
        name="endpoint",
    ),
    path(
        "success/<str:signed_payment_uid>/",
        views.PaymentSuccessView.as_view(),
        name="success",
    ),
    path(
        "webhook/",
        views.PaymentWebhookView.as_view(),
        name="webhook",
    ),
]
