import logging

from django.core.cache import cache
from django.db import connection
from rest_framework import status
from rest_framework.response import Response

logger = logging.getLogger("Project")


class CachedModelViewSetMixin:
    """
    Mixin for DRF ModelViewSet to provide robust Redis caching for CRUD operations.
    Prefixes all cache keys by the tenant schema to guarantee absolute data isolation.
    """

    @property
    def cache_prefix(self):
        # Generates a prefix based on schema name and model name: "public_globalcategory"
        model_name = self.get_queryset().model.__name__.lower()
        return f"{connection.schema_name}_{model_name}"

    def list(self, request, *args, **kwargs):
        cache_key = f"{self.cache_prefix}_list"
        cached_data = cache.get(cache_key)
        if cached_data is not None:
            logger.info(f"Cache HIT for list view: {cache_key}")
            return Response(cached_data)

        logger.info(f"Cache MISS for list view: {cache_key}")
        response = super().list(request, *args, **kwargs)
        if response.status_code == 200:
            cache.set(cache_key, response.data, timeout=60 * 15)
        return response

    def retrieve(self, request, *args, **kwargs):
        instance_id = kwargs.get("pk")
        cache_key = f"{self.cache_prefix}_detail_{instance_id}"
        cached_data = cache.get(cache_key)
        if cached_data is not None:
            logger.info(f"Cache HIT for item view: {cache_key}")
            return Response(cached_data)

        logger.info(f"Cache MISS for item view: {cache_key}")
        response = super().retrieve(request, *args, **kwargs)
        if response.status_code == 200:
            cache.set(cache_key, response.data, timeout=60 * 15)
        return response

    def _invalidate_cache(self, instance_id=None):
        # Invalidate the list cache
        cache.delete(f"{self.cache_prefix}_list")
        # Invalidate the detail cache if instance ID is provided
        if instance_id:
            cache.delete(f"{self.cache_prefix}_detail_{instance_id}")

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        if response.status_code == status.HTTP_201_CREATED:
            self._invalidate_cache()
        return response

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        if response.status_code in [status.HTTP_200_OK, status.HTTP_204_NO_CONTENT]:
            self._invalidate_cache(instance_id=kwargs.get("pk"))
        return response

    def destroy(self, request, *args, **kwargs):
        instance_id = kwargs.get("pk")
        response = super().destroy(request, *args, **kwargs)
        if response.status_code == status.HTTP_204_NO_CONTENT:
            self._invalidate_cache(instance_id=instance_id)
        return response
