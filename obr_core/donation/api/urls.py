from django.urls import path

from . import views

app_name = "donation"
urlpatterns = [
    path(
        "single/create/",
        views.SingleDonationCreateView.as_view(),
        name="donation-single-create",
    ),
    path(
        "single/return/",  # NOTE: called in case of redirect
        views.SingleDonationReturnView.as_view(),
        name="donation-single-return",
    ),
    path(
        "single/<str:payment_intent_id>/finalize/",  # NOTE: called from browser
        views.SingleDonationFinalizeView.as_view(),
        name="donation-single-finalize",
    ),
    path(
        "recurring/options/",
        views.RecurringDonationOptionsView.as_view(),
        name="donation-recurring-options",
    ),
    path(
        "recurring/create/",
        views.RecurringDonationCreateView.as_view(),
        name="donation-recurring-create",
    ),
    path(
        "recurring/return/",  # NOTE: called in case of redirect
        views.RecurringDonationReturnView.as_view(),
        name="donation-recurring-return",
    ),
    path(
        "recurring/<str:payment_intent_id>/finalize/",  # NOTE: called from browser
        views.RecurringDonationFinalizeView.as_view(),
        name="donation-recurring-finalize",
    ),
]
