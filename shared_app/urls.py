from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import GlobalCategoryViewSet

router = DefaultRouter()
router.register(r"categories", GlobalCategoryViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
