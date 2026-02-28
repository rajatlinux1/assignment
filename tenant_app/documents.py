from django.db import connection
from django_elasticsearch_dsl import Document
from django_elasticsearch_dsl.registries import registry
from elasticsearch_dsl import Index

from .models import Item


@registry.register_document
class ItemDocument(Document):

    class Index:
        name = "items"  # keep static

    class Django:
        model = Item
        fields = [
            "id",
            "name",
            "sku",
            "price",
        ]

    @classmethod
    def get_index(cls):
        schema = connection.schema_name
        return Index(f"{schema}_items")
