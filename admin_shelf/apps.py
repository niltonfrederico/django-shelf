from django.apps import AppConfig


class DjangoAdminShelfConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "admin_shelf"

    def ready(self) -> None:
        # Register the custom admin site
        from django.contrib import admin

        from admin_shelf.admin import CategorizedAdminSite

        admin.site.__class__ = CategorizedAdminSite
