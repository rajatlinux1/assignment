from django.contrib import admin
from django.utils.html import format_html

from .models import Client


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "schema_name",
        "domain_url",
        "created_on",
        "manage_tenant_link",
    )
    search_fields = ("name", "schema_name", "domain_url")

    def manage_tenant_link(self, obj):
        if obj.schema_name == "public":
            return "N/A"
        url = f"http://{obj.domain_url}:8000/admin/"
        return format_html('<a href="{}" target="_blank">Manage Tenant Users</a>', url)

    manage_tenant_link.short_description = "Manage Tenant"
