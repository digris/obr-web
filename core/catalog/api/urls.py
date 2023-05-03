from django.urls import include, path

from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r"moods", views.MoodViewSet)
router.register(r"artists", views.ArtistViewSet)
router.register(r"media", views.MediaViewSet)
router.register(r"releases", views.ReleaseViewSet)
router.register(r"playlists", views.PlaylistViewSet)

app_name = "catalog"
urlpatterns = [
    path("", include(router.urls)),
    path(
        "masters/download/<str:uid>/",
        views.MasterDownloadView.as_view(),
        name="master-download",
    ),
]
