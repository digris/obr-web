from django.urls import path

from . import views

app_name = "subscription:voucher"
urlpatterns = [
    path(
        "<str:voucher>",
        views.claim_voucher_view,
        name="claim-voucher",
    ),
]
