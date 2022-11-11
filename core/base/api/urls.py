from django.urls import path

from . import views

app_name = "base"
urlpatterns = [
    path(
        "version/",
        views.VersionView.as_view(),
        name="version",
    ),
    path(
        "settings/",
        views.SettingsView.as_view(),
        name="settings",
    ),
]
