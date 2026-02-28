from django.core.management import call_command
from django.core.management.base import BaseCommand
from django_elasticsearch_dsl.registries import registry
from tenant_schemas.utils import get_tenant_model, schema_context


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument(
            "schema", nargs="?", type=str, help="Schema name to rebuild index for"
        )

    def handle(self, *args, **options):
        TenantModel = get_tenant_model()
        schema_name = options.get("schema")
        print("schema_name = ", schema_name)

        if schema_name:
            tenants = TenantModel.objects.filter(schema_name=schema_name)
            if not tenants.exists():
                self.stdout.write(self.style.ERROR(f"Schema '{schema_name}' not found"))
                return
        else:
            tenants = TenantModel.objects.exclude(schema_name="public")

        for tenant in tenants:
            self.stdout.write(f"\nRebuilding for {tenant.schema_name}")

            with schema_context(tenant.schema_name):

                # Dynamically change index name before rebuild
                for doc in registry.get_documents():
                    doc._index._name = f"{tenant.schema_name}_items"

                call_command("search_index", "--rebuild", "-f")

        self.stdout.write(self.style.SUCCESS("Rebuild completed"))
