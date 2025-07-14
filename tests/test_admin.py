from collections.abc import Callable

import pytest
from example.admin import Model1Admin
from example.models import Model1

from admin_shelf.admin import (
    CATEGORIZED_ADMIN_SITE_REGISTER,
    Category,
    _sort_apps,
    _sort_models,
    categorized,
)
from admin_shelf.typing import AppDict, ModelDict


@pytest.fixture(autouse=True)
def cleanup_categories():
    yield
    CATEGORIZED_ADMIN_SITE_REGISTER.clear()


@pytest.fixture
def category() -> Category:
    return Category(name="Test Category", order=1)


@pytest.fixture
def categorized_app_dict(category: Category) -> AppDict:
    return {
        "name": "Test App",
        "app_label": "test_app",
        "app_url": "/admin/test_app/",
        "has_module_perms": True,
        "__category__": category,
        "models": [],
    }


@pytest.fixture
def django_app_dict(categorized_app_dict: AppDict) -> AppDict:
    """Fixture for a Django app dictionary with a category."""
    app_dict = categorized_app_dict.copy()
    app_dict.pop("__category__", None)  # type: ignore[misc]
    return app_dict


class TestCategory:
    @pytest.mark.parametrize(
        ("name", "order", "expected_exception"),
        [
            (None, 1, ValueError("Category name must be a string.")),
            ("", 1, ValueError("Category name cannot be an empty string.")),
            ("fake-name", "not-an-integer", TypeError("Order must be an integer.")),
        ],
    )
    def test_should_raise_exception_when_params_are_invalid(
        self, name: str, order: int, expected_exception: Exception
    ):
        with pytest.raises(type(expected_exception), match=str(expected_exception)):
            Category(name=name, order=order)


class TestPrivateFunctions:
    @pytest.fixture
    def app_dict(self, request: pytest.FixtureRequest, fixture_fn: str) -> AppDict:
        return request.getfixturevalue(fixture_fn)

    @pytest.mark.parametrize(
        ("fixture_fn", "expected_order"),
        [
            ("categorized_app_dict", 1),
            ("django_app_dict", 0),
        ],
    )
    def test_should_get_order_when_categorized_or_not(
        self, request: pytest.FixtureRequest, fixture_fn: str, expected_order: int
    ):
        app_dict = request.getfixturevalue(fixture_fn)
        assert _sort_apps(app_dict) == expected_order

    @pytest.mark.parametrize(
        ("fixture_fn", "expected_lambda", "expected_order"),
        [
            ("categorized_app_dict", lambda model: model.get("order", 0), 1),
            ("django_app_dict", lambda model: model.get("name", "").lower(), 0),
        ],
    )
    def test_should_return_correct_callable_when_categorized(
        self,
        request: pytest.FixtureRequest,
        fixture_fn: str,
        expected_lambda: Callable,
        expected_order: int,
    ):
        app_dict = request.getfixturevalue(fixture_fn)
        model_dict: ModelDict = {
            "model": Model1,
            "name": "Test Model",
            "object_name": "TestModel",
            "perms": {"add": True, "change": True, "delete": True, "view": True},
            "admin_url": "/admin/test_app/testmodel/",
            "add_url": "/admin/test_app/testmodel/add/",
            "view_only": False,
            "category": app_dict.get("__category__"),
            "order": expected_order,
        }
        assert _sort_models(app_dict)(model_dict) == expected_lambda(model_dict)


class TestCategorizedDecorator:
    def test_should_raise_type_error_when_decorated_class_is_not_model_admin(
        self, category: Category
    ):
        with pytest.raises(ValueError, match="Wrapped class must subclass ModelAdmin."):

            @category.register(Model1)  # type: ignore
            class NotModelAdmin:
                pass

    def test_should_return_already_registered_model_admin(self, category: Category):
        assert categorized(category, 123)(Model1Admin) == Model1Admin
