from django.urls import path
from . import views

app_name = "sync"
urlpatterns = [
    path(
        "schedule/",
        views.SyncScheduleView.as_view(),
        name="schedule",
    ),
    path(
        "app/",
        views.SyncAppView.as_view(),
        name="app",
    ),
]
