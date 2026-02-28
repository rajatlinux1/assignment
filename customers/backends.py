from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db import connection
from tenant_schemas.utils import schema_context


class TenantSuperuserBackend(ModelBackend):
    """
    Allows a superuser defined in the public schema to automatically log into any
    tenant's admin dashboard by synchronizing their user account upon login.
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        if connection.schema_name == "public":
            return None

        User = get_user_model()

        # Check if they exist as a superuser in the public schema
        with schema_context("public"):
            try:
                public_user = User.objects.get(username=username)
                if not (
                    public_user.check_password(password) and public_user.is_superuser
                ):
                    return None
            except User.DoesNotExist:
                return None

        # Sync to the tenant schema explicitly allowing them admin access
        tenant_user, created = User.objects.update_or_create(
            username=public_user.username,
            defaults={
                "email": public_user.email,
                "is_staff": True,
                "is_superuser": True,
                "is_active": True,
                "password": public_user.password,  # Ensure hash matches, though we already validated
            },
        )
        return tenant_user
