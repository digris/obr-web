from django.urls import path

from . import views

app_name = "well_known"
urlpatterns = [
    path(
        "apple-app-site-association",
        views.apple_app_site_association,
        name="apple-app-site-association",
    ),
]
