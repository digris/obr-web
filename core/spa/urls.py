# -*- coding: utf-8 -*-
from django.conf import settings
from django.urls import path, re_path

from . import views

PATH_REGEXP = "[0-9A-Za-z-_.//]+"

if settings.APPEND_SLASH:
    regexp = r"^(?P<path>%s)/$" % PATH_REGEXP
else:
    regexp = r"^(?P<path>%s)$" % PATH_REGEXP

app_name = "spa"
urlpatterns = [
    path(
        "",
        views.SPAIndexView.as_view(),
        name="spa-index",
    ),
    re_path(
        regexp,
        views.SPAIndexView.as_view(),
        name="spa-page",
    ),
]
