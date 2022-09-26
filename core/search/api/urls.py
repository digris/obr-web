from django.urls import path

from . import views

app_name = "search"
urlpatterns = [
    path(
        "global/media/",
        views.GlobalMediaSearchView.as_view({"get": "list"}),
        name="global-media-search",
    ),
]
