from django.urls import path

from . import views

# router = routers.DefaultRouter()
# router.register(r"users", views.UserViewSet)

app_name = "account"
urlpatterns = [
    path(
        "login/",
        views.LoginView.as_view(),
        name="login",
    ),
    path(
        "send-email-login/",
        views.SendEmailLoginView.as_view(),
        name="send-email-login",
    ),
    path(
        "token-login/",
        views.TokenLoginView.as_view(),
        name="token-login",
    ),
    path(
        "signed-email-login/",
        views.SignedEmailLoginView.as_view(),
        name="signed-email-login",
    ),
    path(
        "signed-login-credentials/",
        views.SignedLoginCredentialsView.as_view(),
        name="signed-login-credentials",
    ),
    path(
        "logout/",
        views.LogoutView.as_view(),
        name="logout",
    ),
    path(
        "users/me/",
        views.UserView.as_view(),
        name="current-user",
    ),
    path(
        "email/",
        views.EmailUpdateView.as_view(),
        name="email",
    ),
    path(
        "password/",
        views.PasswordUpdateView.as_view(),
        name="password",
    ),
    path(
        "address/",
        views.AddressUpdateView.as_view(),
        name="address",
    ),
    path(
        "social-backends/",
        views.SocialBackendListView.as_view(),
        name="social-backends",
    ),
    path(
        "social-backends/<str:provider>/<str:uid>/",
        views.SocialBackendDetailView.as_view(),
        name="social-backends-detail",
    ),
    path(
        "address-countries/",
        views.AddressCountries.as_view(),
        name="address-countries",
    ),
]
