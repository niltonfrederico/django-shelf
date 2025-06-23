from collections.abc import Callable
from typing import NamedTuple, TypedDict, cast

from django.contrib.admin import ModelAdmin
from django.contrib.admin.sites import AdminSite
from django.db.models import Model
from django.http import HttpRequest
from django.http.response import HttpResponse
from django.utils.text import slugify


class ModelCategory(NamedTuple):
    category: str
    model_admin_class: type[ModelAdmin]  # type: ignore[type-arg]
    order: int


class ModelAppList(TypedDict):
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


class AppListItem(TypedDict):
    name: str
    app_label: str
    app_url: str
    has_module_perms: bool
    __is_category__: bool | None
    models: list[ModelAppList]


class ModelAdminItem(TypedDict):
    name: str
    model_admin_class: type[ModelAdmin]  # type: ignore[type-arg]
    order: int


CATEGORIZED_ADMIN_SITE_REGISTER: dict[type[ModelAdmin] | None, ModelCategory] = {}  # type: ignore[type-arg]


class CategorizedAdminSite(AdminSite):
    def catch_all_view(self, request: HttpRequest, url: str) -> HttpResponse:
        app_list = self.get_app_list(request)

        for app in app_list:
            # If the URL matches a category, redirect to that category
            if app.get("__is_category__") and slugify(app["name"]) in url:
                return self.app_index(request, app_label=app["app_label"])

        return super().catch_all_view(request, url)

    def get_app_list(
        self, request: HttpRequest, app_label: str | None = None
    ) -> list[AppListItem]:
        app_list = super().get_app_list(request)
        categorized_apps = {}

        for app in app_list:
            categorized_apps[app["app_label"]] = app
            _cached_models = app["models"].copy()
            app["models"] = []
            self._categorize_models(_cached_models, categorized_apps, app)

        # Remove empty categories
        categorized_apps = {
            app_label: app
            for app_label, app in categorized_apps.items()
            if app["models"]
        }

        # Sort models within each category
        for app in categorized_apps.values():
            app["models"].sort(key=lambda model: model.get("order", 999))

        if app_label:
            return [categorized_apps[app_label]]

        return cast(list[AppListItem], categorized_apps.values())

    def _categorize_models(
        self,
        models: list[ModelAppList],
        categorized_apps: dict[str, AppListItem],
        app: AppListItem,
    ) -> None:
        for model in models:
            model_admin_instance = self._registry.get(model["model"])
            model_admin_class = (
                type(model_admin_instance) if model_admin_instance else None
            )

            if model_category := CATEGORIZED_ADMIN_SITE_REGISTER.get(model_admin_class):
                if model_category.category not in categorized_apps:
                    categorized_apps[model_category.category] = AppListItem(
                        name=model_category.category,
                        app_label=model_category.category,
                        app_url=f"/admin/{slugify(model_category.category)}/",
                        __is_category__=True,
                        has_module_perms=True,
                        models=[],
                    )

                model["order"] = model_category.order
                model["category"] = model_category.category

                categorized_apps[model_category.category]["models"].append(model)
            else:
                categorized_apps[app["app_label"]]["models"].append(model)


# Categorized decorator
# Decorator to add an Admin model to a specific category
def categorized(
    category: str, order: int = 999
) -> Callable[[type[ModelAdmin]], type[ModelAdmin]]:  # type: ignore[type-arg]
    def decorator(model_admin_class: type[ModelAdmin]) -> type[ModelAdmin]:  # type: ignore[type-arg]
        if not issubclass(model_admin_class, ModelAdmin):
            raise TypeError("The decorated class must be a subclass of ModelAdmin.")

        if model_admin_class in CATEGORIZED_ADMIN_SITE_REGISTER:
            return model_admin_class

        CATEGORIZED_ADMIN_SITE_REGISTER[model_admin_class] = ModelCategory(
            category=category,
            model_admin_class=model_admin_class,
            order=order,
        )

        return model_admin_class

    return decorator
