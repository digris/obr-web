# -*- coding: utf-8 -*-

from django.urls import include, path
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r"artists", views.ArtistViewSet)
router.register(r"media", views.MediaViewSet)
router.register(r"releases", views.ReleaseViewSet)
router.register(r"playlists", views.PlaylistViewSet)

app_name = "catalog"
urlpatterns = [
    path("", include(router.urls)),
]
