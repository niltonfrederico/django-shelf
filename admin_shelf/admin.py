from collections.abc import Callable
from typing import cast

from django.contrib.admin import ModelAdmin
from django.contrib.admin.decorators import register as django_register
from django.contrib.admin.sites import AdminSite
from django.db.models import Model
from django.http import HttpRequest
from django.http.response import HttpResponse
from django.utils.text import slugify

from admin_shelf import settings
from admin_shelf.typing import AppDict, CategorizedModel, ModelDict

CATEGORIZED_ADMIN_SITE_REGISTER: dict[type[ModelAdmin] | None, CategorizedModel] = {}


class Category:
    name: str
    order: int

    def __init__(self, name: str, order: int = settings.CATEGORY_DEFAULT_ORDER):
        if not isinstance(name, str):
            raise ValueError("Category name must be a string.")

        if not name.strip():
            raise ValueError("Category name cannot be an empty string.")

        if not isinstance(order, int):
            raise TypeError("Order must be an integer.")

        self.name = name
        self.order = order


def _sort_apps(app: AppDict) -> int:
    """
    Sort function for apps in the admin interface.

    All apps without order are considered to have an order of 0.
    """
    if category := app.get("__category__"):
        return category.order or 0

    return 0


def _sort_models(app: AppDict) -> Callable:
    if app.get("__category__"):
        return lambda model: model.get("order", 0)

    return lambda model: model.get("name", "").lower()


class CategorizedAdminSite(AdminSite):
    """
    A custom Django AdminSite that categorizes models into categories based on
    the `categorized` decorator. This allows for better organization of models
    in the Django admin interface.
    """

    def catch_all_view(self, request: HttpRequest, url: str) -> HttpResponse:
        app_list = self.get_app_list(request)
        url_segments = [segment for segment in url.strip("/").split("/") if segment]

        for app in app_list:
            # If the URL matches a category, fake an app_index call
            if app.get("__category__") and slugify(app["name"]) in url_segments:
                return self.app_index(request, app_label=app["app_label"])

        return super().catch_all_view(request, url)

    def get_app_list(
        self, request: HttpRequest, app_label: str | None = None
    ) -> list[AppDict]:
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

        app_list = cast(list[AppDict], list(categorized_apps.values()))

        # Sort categories by order, then by name
        app_list.sort(key=_sort_apps)

        # Sort models within each category
        for app in app_list:
            sort_key = _sort_models(app)
            app["models"].sort(key=sort_key)

        if app_label:
            return [categorized_apps[app_label]]

        return app_list

    def _categorize_models(
        self,
        models: list[ModelDict],
        categorized_apps: dict[str, AppDict],
        app: AppDict,
    ) -> None:
        for model in models:
            model_admin_instance = self._registry.get(model["model"])
            model_admin_class = (
                type(model_admin_instance) if model_admin_instance else None
            )

            keep_app = True
            if model_category := CATEGORIZED_ADMIN_SITE_REGISTER.get(model_admin_class):
                if model_category.category.name not in categorized_apps:
                    categorized_apps[model_category.category.name] = AppDict(
                        name=model_category.category.name,
                        app_label=model_category.category.name,
                        app_url=f"/admin/{slugify(model_category.category.name)}/",
                        __category__=model_category.category,
                        has_module_perms=True,
                        models=[],
                    )

                model["order"] = model_category.order
                model["category"] = model_category.category

                categorized_apps[model_category.category.name]["models"].append(model)

                if settings.HIDE_CATEGORIZED_MODELS:
                    keep_app = False

            if keep_app:
                categorized_apps[app["app_label"]]["models"].append(model)


# Categorized decorator
# Decorator to add an Admin model to a specific category
def categorized(
    category: Category, order: int = settings.MODEL_DEFAULT_ORDER
) -> Callable[[type[ModelAdmin]], type[ModelAdmin]]:
    """
    Decorator to categorize a ModelAdmin class into a specific category.
    The `category` argument is the name of the category, and `order` is the
    order in which the category should appear in the admin interface.
    """

    def decorator(model_admin_class: type[ModelAdmin]) -> type[ModelAdmin]:
        if not issubclass(model_admin_class, ModelAdmin):
            raise TypeError("The decorated class must be a subclass of ModelAdmin.")

        if model_admin_class in CATEGORIZED_ADMIN_SITE_REGISTER:
            return model_admin_class

        CATEGORIZED_ADMIN_SITE_REGISTER[model_admin_class] = CategorizedModel(
            category=category,
            model_admin_class=model_admin_class,
            order=order,
        )

        return model_admin_class

    return decorator


def categorized_register(
    *models: type[Model],
    site: AdminSite | None = None,
    category: Category | None = None,
    order: int = settings.MODEL_DEFAULT_ORDER,
) -> Callable[[type[ModelAdmin]], type[ModelAdmin]]:
    """
    Decorator to register a ModelAdmin class for one or more models with
    categorization support. The `category` argument is the name of the category,
    and `order` is the order in which the category should appear in the admin interface.
    If `category` is None, the model will be registered without categorization.
    """

    def wrapper(
        model_admin_class: type[ModelAdmin],
    ) -> type[ModelAdmin]:
        admin_register_decorator = django_register(*models, site=site)
        decorated_admin_class = admin_register_decorator(model_admin_class)

        if category is not None:
            return categorized(category, order)(decorated_admin_class)

        return decorated_admin_class

    return wrapper


register = categorized_register  # Alias for convenience
