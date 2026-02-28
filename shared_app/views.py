from rest_framework import viewsets

from Project.mixins import CachedModelViewSetMixin

from .models import GlobalCategory
from .serializers import GlobalCategorySerializer


class GlobalCategoryViewSet(CachedModelViewSetMixin, viewsets.ModelViewSet):
    queryset = GlobalCategory.objects.all()
    serializer_class = GlobalCategorySerializer
