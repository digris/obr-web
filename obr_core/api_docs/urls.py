from django.urls import path

from .views import api_docs

app_name = "api_docs"
urlpatterns = [
    path("", api_docs, name="scalar"),
]
