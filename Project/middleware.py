from django.conf import settings
from django.db import connection
from django.http import Http404
from tenant_schemas.middleware import BaseTenantMiddleware
from tenant_schemas.utils import get_tenant_model


class CustomTenantMiddleware(BaseTenantMiddleware):
    """
    Middleware that resolves the tenant primarily using the X-Tenant-Id header,
    falling back to processing the hostname if the header is not present.
    """

    def get_tenant(self, model, hostname, request):
        tenant_header = request.headers.get("X-Tenant-Id")

        if tenant_header:
            try:
                # Resolve tenant by the header value (e.g., 'test', 'client_a', 'public')
                tenant = model.objects.get(schema_name=tenant_header)

                # Assign the correct domain_url to avoid issues with standard django-tenant-schemas logic
                if not hasattr(tenant, "domain_url") or not tenant.domain_url:
                    tenant.domain_url = request.get_host()
                return tenant
            except model.DoesNotExist:
                # Fallback to hostname resolution if the tenant from the header doesn't exist
                pass

        # Default django-tenant-schemas behavior mapping hostname to domain_url
        return model.objects.get(domain_url=hostname)
