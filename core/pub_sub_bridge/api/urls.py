# -*- coding: utf-8 -*-

from django.urls import path
from . import views


app_name = "pub_sub_bridge"
urlpatterns = [
    path("", views.BridgeView.as_view()),
]
