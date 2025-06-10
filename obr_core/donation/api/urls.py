from django.urls import path

from . import views

app_name = "donation"
urlpatterns = [
    path(
        "create/",
        views.DonationCreateView.as_view(),
        name="donation-create",
    ),
    path(
        "return/",  # NOTE: called in case of redirect
        views.DonationReturnView.as_view(),
        name="donation-return",
    ),
    path(
        "<str:payment_intent_id>/finalize/",  # NOTE: called from browser
        views.DonationFinalizeView.as_view(),
        name="donation-finalize",
    ),
    path(
        "options/",
        views.DonationOptionsView.as_view(),
        name="donation-options",
    ),
]
