from django.urls import path

from . import views

app_name = "survey"
urlpatterns = [
    path(
        "news/",
        views.NewsSurveySubmissionView.as_view(),
        name="news",
    ),
]
