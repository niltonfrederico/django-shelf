from typing import TypedDict

from django.conf import settings as django_settings


class Settings(TypedDict):
    """
    Settings typing for the Django Shelf application.
    """

    """
    HIDE_CATEGORIZED_MODELS: bool
        Determines whether categorized models should be hidden from the
        default app list in the Django admin interface.
    """
    HIDE_CATEGORIZED_MODELS: bool

    """
    CATEGORY_DEFAULT_ORDER: int
        The default order for categories in the Django Shelf admin.
        If not specified, it defaults to 0 (which will cause them to be sorted by name).
    """
    CATEGORY_DEFAULT_ORDER: int

    """
    MODEL_DEFAULT_ORDER: int
        The default order for models inside an app in the Django Shelf admin.
        If not specified, it defaults to 0 (which will cause them to be sorted by name).
    """
    MODEL_DEFAULT_ORDER: int


default_settings = Settings(
    HIDE_CATEGORIZED_MODELS=True,
    CATEGORY_DEFAULT_ORDER=0,
    MODEL_DEFAULT_ORDER=0,
)

DJANGO_ADMIN_SHELF = getattr(django_settings, "DJANGO_ADMIN_SHELF", default_settings)
settings: Settings = default_settings | DJANGO_ADMIN_SHELF


HIDE_CATEGORIZED_MODELS = settings["HIDE_CATEGORIZED_MODELS"]
CATEGORY_DEFAULT_ORDER = settings["CATEGORY_DEFAULT_ORDER"]
MODEL_DEFAULT_ORDER = settings["MODEL_DEFAULT_ORDER"]
