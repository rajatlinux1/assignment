from django.urls import path

from .views import product_catalog_view

urlpatterns = [
    path("", product_catalog_view, name="product-catalog"),
]
