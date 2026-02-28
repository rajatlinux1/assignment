import json
from unittest.mock import patch, MagicMock

from django.test import TestCase, RequestFactory
from django.urls import reverse
from tenant_schemas.utils import tenant_context

from customers.models import Client
from tenant_app.views import product_catalog_view


class TestProductCatalogView(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.url = reverse("product-catalog")
        self.tenant, _ = Client.objects.get_or_create(
            schema_name="test_catalog",
            defaults={"domain_url": "testcatalog.localhost", "name": "Test Catalog Tenant"},
        )

    @patch("tenant_app.views.ItemDocument.search")
    def test_product_catalog_view_html(self, mock_search):
        """Test the standard HTML render response of the product catalog filter."""
        mock_response = MagicMock()
        mock_response.hits.total.value = 1
        
        mock_hit = MagicMock()
        mock_hit.id = "1"
        mock_hit.name = "Test HTML Product"
        mock_hit.price = 10.50
        mock_hit.sku = "TEST-HTML-1"
        
        mock_response.__iter__.return_value = [mock_hit]

        mock_search_instance = MagicMock()
        mock_search.return_value = mock_search_instance
        mock_search_instance.query.return_value = mock_search_instance
        mock_search_instance.__getitem__.return_value = mock_search_instance
        mock_search_instance.execute.return_value = mock_response

        with tenant_context(self.tenant):
            request = self.factory.get(self.url)
            request.tenant = self.tenant 
            
            response = product_catalog_view(request)
            
            self.assertEqual(response.status_code, 200)
            content = response.content.decode("utf-8")
            self.assertIn("Test HTML Product", content)
            self.assertIn("10.5", content)
            self.assertIn("TEST-HTML-1", content)
            
            mock_search_instance.query.assert_called_with("match_all")

    @patch("tenant_app.views.ItemDocument.search")
    def test_product_catalog_view_ajax(self, mock_search):
        """Test the AJAX/JSON response mapping of the product catalog filter."""
        mock_response = MagicMock()
        mock_response.hits.total.value = 1
        
        mock_hit = MagicMock()
        mock_hit.id = "2"
        mock_hit.name = "Test Ajax Product"
        mock_hit.price = 25.00
        mock_hit.sku = "TEST-AJAX-1"
        
        mock_response.__iter__.return_value = [mock_hit]
        
        mock_search_instance = MagicMock()
        mock_search.return_value = mock_search_instance
        mock_search_instance.query.return_value = mock_search_instance
        mock_search_instance.__getitem__.return_value = mock_search_instance
        mock_search_instance.execute.return_value = mock_response

        with tenant_context(self.tenant):
            # Pass AJAX parameters via request object
            request = self.factory.get(self.url, {"ajax": "1", "q": "AjaxQuery"})
            request.tenant = self.tenant
            
            response = product_catalog_view(request)
            
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response["Content-Type"], "application/json")
            
            data = json.loads(response.content)
            self.assertEqual(data["total"], 1)
            self.assertEqual(len(data["products"]), 1)
            self.assertEqual(data["products"][0]["name"], "Test Ajax Product")
            self.assertEqual(data["products"][0]["sku"], "TEST-AJAX-1")
            
            # Verify the view applied the phrase_prefix 'multi_match' elasticsearch logic correctly
            mock_search_instance.query.assert_called_with(
                "multi_match",
                query="AjaxQuery",
                fields=["name^3", "sku"],
                type="phrase_prefix",
            )