from django.urls import path

from . import views

app_name = "app_bridge"
urlpatterns = [
    path(
        "social-auth-redirect/",
        views.social_auth_redirect,
        name="social-auth-redirect",
    ),
]
