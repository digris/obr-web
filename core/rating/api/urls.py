from django.urls import re_path

from . import views

app_name = "rating"
urlpatterns = [
    re_path(
        r"^(?P<obj_ct>[a-z-_\.]+):(?P<obj_uid>[0-9A-F]{8})/$",
        views.ObjectRatingView.as_view(),
        name="object-rating",
    ),
]
