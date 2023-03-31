from django.urls import include, path

from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r"ratings", views.RatingViewSet)

app_name = "stats"
urlpatterns = [
    path("", include(router.urls)),
    path(
        "player-events/",
        views.PlayerEventView.as_view(),
        name="player-events",
    ),
    path(
        "stream-events/",
        views.StreamEventView.as_view(),
        name="stream-events",
    ),
    path(
        "archive/",
        views.StatsArchiveView.as_view(),
        name="archive",
    ),
]
