from typing import NamedTuple, TypedDict

from django.contrib.admin import ModelAdmin
from django.db.models import Model


class CategorizedModel(NamedTuple):
    category: str
    model_admin_class: type[ModelAdmin]
    order: int


class ModelDict(TypedDict):
    model: type[Model]
    name: str
    object_name: str
    perms: dict[str, bool]
    admin_url: str
    add_url: str | None
    view_only: bool

    # Injected by CategorizedAdminSite
    order: int | None
    category: str | None


class AppDict(TypedDict):
    name: str
    app_label: str
    app_url: str
    has_module_perms: bool
    __is_category__: bool | None
    models: list[ModelDict]
