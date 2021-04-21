# -*- coding: utf-8 -*-

from django.urls import path

from . import views

# router = routers.DefaultRouter()
# router.register(r"users", views.UserViewSet)

app_name = "account"
urlpatterns = [
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("users/me/", views.CurrentUserView.as_view(), name="current-user"),
    path(
        "refresh-credentials/",
        views.CredentialsView.as_view(),
        name="refresh-credentials",
    ),
    # path("", include(router.urls)),
]
