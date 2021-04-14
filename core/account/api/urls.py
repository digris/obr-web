# -*- coding: utf-8 -*-

from django.urls import include, path
from rest_framework import routers

from . import views

# router = routers.DefaultRouter()
# router.register(r"users", views.UserViewSet)

app_name = "account"
urlpatterns = [
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("users/me/", views.CurrentUserView.as_view(), name="current-user"),
    # path("", include(router.urls)),
]
