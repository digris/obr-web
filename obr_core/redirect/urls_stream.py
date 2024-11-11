from django.urls import re_path

from . import views

app_name = "redirect:stream"
urlpatterns = [
    re_path(
        r"^(?P<path>.*)$",
        views.stream_redirect_view,
        name="stream-redirect",
    ),
]
