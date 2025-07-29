from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserAuthViewSet

router = DefaultRouter()
router.register(r"auth", UserAuthViewSet, basename="user-auth")

urlpatterns = [
    path("", include(router.urls)),
]
