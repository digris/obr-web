# -*- coding: utf-8 -*-
from django.urls import path

from . import views

app_name = "manifest"
urlpatterns = [
    path(
        "manifest.json",
        views.manifest_view,
        name="manifest",
    ),
]
