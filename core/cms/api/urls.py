from django.urls import path
from . import views

app_name = "cms"
urlpatterns = [
    path(r"page/<path:path>/", views.PageView.as_view(), name="page"),
]
