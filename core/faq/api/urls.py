from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register("categories", views.CategoryViewSet)

app_name = "faq"
urlpatterns = [
    path("", include(router.urls)),
]
