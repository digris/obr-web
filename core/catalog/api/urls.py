# -*- coding: utf-8 -*-

from django.urls import include, path
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r"artists", views.ArtistViewSet)
router.register(r"media", views.MediaViewSet)

app_name = "catalog"
urlpatterns = [
    path("", include(router.urls)),
]
