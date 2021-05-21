# -*- coding: utf-8 -*-
from django.urls import include, path

from . import views
from .stripe import urls as stripe_urls


app_name = "subscription"
urlpatterns = [
    path(
        "",
        views.SubscriptionView.as_view(),
        name="subscription",
    ),
    path(
        "trial/",
        views.SubscriptionTrialView.as_view(),
        name="subscription-trial",
    ),
    path(
        "plan/",
        views.SubscriptionPlanView.as_view(),
        name="subscription-plan",
    ),
    path(
        "payment/",
        views.PaymentView.as_view(),
        name="payment",
    ),
    path("payment/stripe/", include(stripe_urls)),
]
