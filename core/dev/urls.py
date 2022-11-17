from django.urls import path
from . import views

app_name = "dev"
urlpatterns = [
    path("email/login-code/", views.email_login_code),
    path("redirect/", views.redirect),
]
