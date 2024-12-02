from django.urls import path

from . import views

app_name = "qr-redirect"
urlpatterns = [
    path(
        "<str:uid>/",
        views.qr_redirect_view,
        name="redirect",
    ),
]
