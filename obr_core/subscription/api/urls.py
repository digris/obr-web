from django.urls import include, path

from . import views
from .stripe import urls as stripe_urls

app_name = "subscription"
urlpatterns = [
    path(
        "plan/",
        views.PlanView.as_view(),
        name="plan",
    ),
    path(
        "payment/",
        views.PaymentView.as_view(),
        name="payment",
    ),
    path(
        "payment/stripe/",
        include(stripe_urls),
    ),
    path(
        "voucher/",
        views.VoucherView.as_view(),
        name="voucher",
    ),
    path(
        "user-vouchers/",
        views.UserVoucherView.as_view(),
        name="user-vouchers",
    ),
]
