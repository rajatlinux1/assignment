# from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.core.cache import cache
from django.db import connection, models

# from Project.elasticsearch_client import index_document, remove_document


class Item(models.Model):
    name = models.CharField(max_length=100)
    sku = models.CharField(max_length=20, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

    # def _get_cache_prefix(self):
    #     return f"{connection.schema_name}_item"

    # def save(self, *args, **kwargs):
    #     prefix = self._get_cache_prefix()
    #     cache.delete(f'{prefix}_{self.pk}')
    #     cache.delete(f'{prefix}_list')
    #     super().save(*args, **kwargs)

    #     # Sync with Elasticsearch (Isolated Tenant Index)
    #     data = {
    #         'id': self.pk,
    #         'name': self.name,
    #         'sku': self.sku,
    #         'price': float(self.price)
    #     }
    #     try:
    #         index_document('item', self.pk, data)
    #     except Exception as e:
    #         # Log the error but continue; Elasticsearch may be unavailable.
    #         import logging
    #         logger = logging.getLogger(__name__)
    #         logger.warning(f'Elasticsearch indexing failed for Item {self.pk}: {e}')

    #     # Broadcast real-time WebSockets notification
    #     channel_layer = get_channel_layer()
    #     if channel_layer:
    #         async_to_sync(channel_layer.group_send)(
    #             f'notifications_{connection.schema_name}',
    #             {
    #                 'type': 'send_notification',
    #                 'message': f"Item saved: {self.name} (SKU: {self.sku})"
    #             }
    #         )

    # def delete(self, *args, **kwargs):
    #     prefix = self._get_cache_prefix()
    #     cache.delete(f'{prefix}_{self.pk}')
    #     cache.delete(f'{prefix}_list')

    #     # Remove from Elasticsearch (Isolated Tenant Index)
    #     remove_document('item', self.pk)

    #     super().delete(*args, **kwargs)

    # @classmethod
    # def get_cached(cls, pk):
    #     prefix = f"{connection.schema_name}_item"
    #     cache_key = f'{prefix}_{pk}'
    #     obj = cache.get(cache_key)
    #     if obj is None:
    #         obj = cls.objects.get(pk=pk)
    #         cache.set(cache_key, obj, timeout=60*15)
    #     return obj

    # @classmethod
    # def get_all_cached(cls):
    #     prefix = f"{connection.schema_name}_item"
    #     cache_key = f'{prefix}_list'
    #     qs = cache.get(cache_key)
    #     if qs is None:
    #         qs = list(cls.objects.all())
    #         cache.set(cache_key, qs, timeout=60*15)
    #     return qs
