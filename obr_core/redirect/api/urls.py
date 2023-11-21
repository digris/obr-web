from django.urls import re_path

from . import views

app_name = "redirect"
urlpatterns = [
    re_path(
        r"^obp/(?P<obj_ct>[a-z-_\.]+):(?P<obj_uid>[0-9A-F]{8})/$",
        views.OBPRedirectView.as_view(),
        name="obp-object-redirect",
    ),
]
