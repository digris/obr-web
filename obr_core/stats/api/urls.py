from django.urls import include, path

from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r"ratings", views.RatingViewSet)
router.register(r"player-events", views.PlayerEventViewSet)
router.register(r"processed-player-events", views.ProcessedPlayerEventViewSet)
router.register(r"stream-events", views.StreamEventViewSet)

app_name = "stats"
urlpatterns = [
    path("", include(router.urls)),
    path(
        "ingest/player-events/",
        views.PlayerEventCreateView.as_view(),
        name="player-events-create",
    ),
    path(
        "ingest/stream-events/",
        views.StreamEventCreateView.as_view(),
        name="stream-events-create",
    ),
    path(
        "process/player-events/",
        views.PlayerEventProcessView.as_view(),
        name="player-events-process",
    ),
    path(
        "heartbeat/",
        views.HeartbeatView.as_view(),
        name="heartbeat",
    ),
    path(
        "archive/",
        views.StatsArchiveView.as_view(),
        name="archive",
    ),
]
