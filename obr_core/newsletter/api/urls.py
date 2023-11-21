from django.urls import path

from . import views

app_name = "newsletter"
urlpatterns = [
    path(
        "newsletters/",
        views.NewsletterView.as_view(),
        name="newsletters",
    ),
]
