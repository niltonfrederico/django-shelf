from django.apps import AppConfig


class DjangoShelfConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "django_shelf"

    def ready(self) -> None:
        # Register the custom admin site
        from django.contrib import admin

        from django_shelf.admin import CategorizedAdminSite

        admin.site.__class__ = CategorizedAdminSite
