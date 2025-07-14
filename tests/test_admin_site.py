# noqa: ARG
import pytest
from django.contrib.admin import AdminSite
from django.http import HttpResponse
from django.test import RequestFactory
from example.models import Model1  # Replace with actual models

from admin_shelf.admin import (
    CategorizedAdminSite,
)


class AdminCategory:
    """Mock class to represent admin category"""

    def __init__(self, name, order=0):
        self.name = name
        self.order = order


class MockModelAdmin:
    """Mock model admin for testing"""


class CategoryTest:
    """Test category class"""

    def __init__(self, category, order=0):
        self.category = category
        self.order = order


@pytest.fixture
def categorized_admin_site():
    """Fixture providing a categorized admin site instance."""
    return CategorizedAdminSite(name="categorized_admin")


@pytest.fixture
def request_factory():
    """Fixture providing a request factory."""
    return RequestFactory()


@pytest.fixture
def mock_get_app_list(monkeypatch):
    """Fixture to mock the parent get_app_list method."""

    def mock_super_get_app_list(self, request, app_label=None):
        # Return a mocked app list that simulates parent's behavior
        return [
            {
                "app_label": "app1",
                "name": "Application 1",
                "models": [
                    {
                        "model": Model1,
                        "name": "Test Model",
                        "object_name": "TestModel",
                        "admin_url": "/admin/app1/testmodel/",
                        "view_only": False,
                    }
                ],
                "has_module_perms": True,
                "app_url": "/admin/app1/",
            }
        ]

    monkeypatch.setattr(AdminSite, "get_app_list", mock_super_get_app_list)


@pytest.fixture
def setup_categorized_register(monkeypatch):
    """Setup test categories in the register."""
    category1 = AdminCategory(name="Category 1", order=1)
    category2 = AdminCategory(name="Category 2", order=2)

    # Create mock register data
    mock_register = {
        MockModelAdmin: CategoryTest(category=category1, order=1),
    }

    # Replace the actual register with our mock
    monkeypatch.setattr(
        "admin_shelf.admin.CATEGORIZED_ADMIN_SITE_REGISTER", mock_register
    )

    return {
        "category1": category1,
        "category2": category2,
    }


class TestCategorizedAdminSite:
    """Test class for CategorizedAdminSite."""

    def test_catch_all_view_with_category_url(
        self, categorized_admin_site, request_factory, monkeypatch
    ):
        """Test catch_all_view when URL contains a category slug."""
        # Setup
        request = request_factory.get("/admin/category-1/")

        # Mock app_index to track if it gets called
        called_with = {}

        def mock_app_index(request, app_label=None):
            called_with["app_label"] = app_label
            return HttpResponse("Mocked app_index")

        # Bind the method to the instance
        categorized_admin_site.app_index = mock_app_index

        # Mock get_app_list to return categories
        def mock_get_app_list(request):
            return [
                {
                    "app_label": "app1",
                    "name": "Category 1",
                    "__category__": True,
                    "models": [],
                }
            ]

        # Bind the method to the instance
        categorized_admin_site.get_app_list = mock_get_app_list

        # Execute
        response = categorized_admin_site.catch_all_view(request, "category-1/")

        # Assert
        assert called_with.get("app_label") == "app1"
        assert isinstance(response, HttpResponse)

    def test_catch_all_view_with_non_category_url(
        self, categorized_admin_site, request_factory, monkeypatch
    ):
        """Test catch_all_view when URL is not a category."""
        # Setup
        request = request_factory.get("/admin/non-category/")

        # Mock parent catch_all_view
        def mock_super_catch_all_view(self, request, url):
            return HttpResponse("Super catch_all_view")

        monkeypatch.setattr(AdminSite, "catch_all_view", mock_super_catch_all_view)

        # Mock get_app_list
        def mock_get_app_list(request):
            return [{"app_label": "app1", "name": "App 1", "models": []}]

        categorized_admin_site.get_app_list = mock_get_app_list

        # Execute
        response = categorized_admin_site.catch_all_view(request, "non-category/")

        # Assert
        assert response.content == b"Super catch_all_view"

    def test_get_app_list_categorizes_models(
        self,
        categorized_admin_site,
        request_factory,
        mock_get_app_list,
        setup_categorized_register,
    ):
        """Test that get_app_list properly categorizes models."""
        # Setup
        request = request_factory.get("/admin/")

        # Mock _registry to return our mock model admin
        categorized_admin_site._registry = {Model1: MockModelAdmin()}

        # Execute
        result = categorized_admin_site.get_app_list(request)

        # Assert
        # We should have two categories: original app and our custom category
        assert len(result) > 0

        # Check if categorization happened
        category_found = False
        for app in result:
            if app.get("__category__"):
                category_found = True
                break

        assert category_found

    def test_get_app_list_with_specific_app_label(
        self, categorized_admin_site, request_factory, mock_get_app_list
    ):
        """Test get_app_list when app_label is provided."""
        # Setup
        request = request_factory.get("/admin/app1/")

        # Execute
        result = categorized_admin_site.get_app_list(request, app_label="app1")

        # Assert
        assert len(result) == 1
        assert result[0]["app_label"] == "app1"

    def test_categorize_models(
        self, categorized_admin_site, setup_categorized_register, monkeypatch
    ):
        """Test the _categorize_models method."""
        # Setup
        models = [
            {
                "model": Model1,
                "name": "Test Model",
                "object_name": "TestModel",
                "admin_url": "/admin/app1/testmodel/",
                "view_only": False,
            }
        ]

        categorized_apps = {
            "app1": {
                "app_label": "app1",
                "name": "App 1",
                "models": [],
                "has_module_perms": True,
                "app_url": "/admin/app1/",
            }
        }

        app = categorized_apps["app1"]

        # Mock settings
        class MockSettings:
            HIDE_CATEGORIZED_MODELS = False

        monkeypatch.setattr("admin_shelf.admin.settings", MockSettings())

        # Mock _registry
        categorized_admin_site._registry = {Model1: MockModelAdmin()}

        # Execute
        categorized_admin_site._categorize_models(models, categorized_apps, app)

        # Assert
        # Verify models were properly categorized
        category_name = setup_categorized_register["category1"].name
        assert category_name in categorized_apps
        assert len(categorized_apps[category_name]["models"]) > 0  # type: ignore

        # Original app should still have models if HIDE_CATEGORIZED_MODELS is False
        assert len(categorized_apps["app1"]["models"]) > 0  # type: ignore
