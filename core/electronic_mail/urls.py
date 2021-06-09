# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.urls import path

from . import views

app_name = "electronic_mail"
urlpatterns = [
    path(
        "preview/",
        views.email_preview,
    ),
]