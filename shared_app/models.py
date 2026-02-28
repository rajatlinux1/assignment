from django.core.cache import cache
from django.db import models


class GlobalCategory(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Invalidate cache for this item and the list
        cache.delete(f"globalcategory_{self.pk}")
        cache.delete("globalcategory_list")
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Invalidate cache for this item and the list
        cache.delete(f"globalcategory_{self.pk}")
        cache.delete("globalcategory_list")
        super().delete(*args, **kwargs)

    @classmethod
    def get_cached(cls, pk):
        cache_key = f"globalcategory_{pk}"
        obj = cache.get(cache_key)
        if obj is None:
            obj = cls.objects.get(pk=pk)
            cache.set(cache_key, obj, timeout=60 * 15)  # Cache for 15 minutes
        return obj

    @classmethod
    def get_all_cached(cls):
        cache_key = "globalcategory_list"
        qs = cache.get(cache_key)
        if qs is None:
            qs = list(cls.objects.all())
            cache.set(cache_key, qs, timeout=60 * 15)
        return qs
