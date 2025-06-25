from django.conf import settings

"""
DJANGO_SHELF_HIDE_CATEGORIZED_MODELS is a setting that determines whether
categorized modelsshould be removed from their default app list in the
Django admin interface.
"""
DJANGO_SHELF_HIDE_CATEGORIZED_MODELS = getattr(
    settings, "DJANGO_SHELF_HIDE_CATEGORIZED_MODELS", True
)

"""
DJANGO_SHELF_CATEGORY_DEFAULT_ORDER is the default order for categories in
the Django Shelf admin. If not specified, it defaults to 0 (which will
cause them to be sorted by name).
"""
DJANGO_SHELF_CATEGORY_DEFAULT_ORDER = getattr(
    settings, "DJANGO_SHELF_CATEGORY_DEFAULT_ORDER", 0
)

"""
DJANGO_SHELF_MODEL_DEFAULT_ORDER is the default order for models inside
an app in the Django Shelf admin. If not specified, it defaults to 0
(which will cause them to be sorted by name
"""
DJANGO_SHELF_MODEL_DEFAULT_ORDER = getattr(
    settings, "DJANGO_SHELF_MODEL_DEFAULT_ORDER", 0
)
