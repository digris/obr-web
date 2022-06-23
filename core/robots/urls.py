from django.urls import path
from . import views

app_name = "robots"

urlpatterns = [
    path("robots.txt", views.robots_txt, name="robots-txt"),
]
