# -*- coding: utf-8 -*-

from django.urls import include, path
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r"editors", views.EditorViewSet)
router.register(r"emissions", views.EmissionViewSet)
# router.register(r"program", views.ProgramView)

app_name = "broadcast"
urlpatterns = [
    path("", include(router.urls)),
    path("schedule/", views.ScheduleView.as_view()),
    path("program/", views.ProgramView.as_view()),
]
