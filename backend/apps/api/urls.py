from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.holter.views import HolterRecordViewSet

router = DefaultRouter()
router.register("holter", HolterRecordViewSet, basename="holter")

urlpatterns = [path("", include(router.urls))]