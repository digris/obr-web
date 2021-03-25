# -*- coding: utf-8 -*-
from django.urls import path

from catalog import views

app_name = "catalog"
urlpatterns = [
    path(
        "media/manifest/<str:uid>/",
        views.MediaManifestRedirectView.as_view(),
        name="media-manifest",
    ),
]
