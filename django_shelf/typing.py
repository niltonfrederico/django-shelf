from typing import TYPE_CHECKING, NamedTuple, TypedDict

from django.contrib.admin import ModelAdmin
from django.db.models import Model

if TYPE_CHECKING:
    from django_shelf.admin import Category


class CategorizedModel(NamedTuple):
    category: "Category"
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
    category: "Category | None"


class AppDict(TypedDict):
    name: str
    app_label: str
    app_url: str
    has_module_perms: bool
    __category__: "Category | None"
    models: list[ModelDict]
