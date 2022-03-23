from django.urls import path

from . import views

app_name = "version"
urlpatterns = [
    path(
        "",
        views.VersionView.as_view(),
        name="version",
    ),
]
