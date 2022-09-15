from django.urls import path

from . import views

app_name = "search"
urlpatterns = [
    path(
        "global/",
        views.GlobalSearchView.as_view(),
        name="global-search",
    ),
]
