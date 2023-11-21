from django.urls import path

from . import views

app_name = "playout"
urlpatterns = [
    path("schedule/", views.ScheduleView.as_view()),
]
