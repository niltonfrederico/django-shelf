from django.contrib.admin.decorators import register as django_register

from django_shelf import admin
from example.models import First, Fourth, Second, Third


@admin.register(First, category="Custom Category")
class FirstAdmin(admin.ModelAdmin):  # type: ignore[type-arg]
    pass


@admin.register(Second, category="Custom Category", order=1)
class SecondAdmin(admin.ModelAdmin):  # type: ignore[type-arg]
    pass


@admin.register(Third, category="Other Category")
class ThirdAdmin(admin.ModelAdmin):  # type: ignore[type-arg]
    pass


@django_register(Fourth)
class FourthAdmin(admin.ModelAdmin):  # type: ignore[type-arg]
    """
    This admin is registered using the `@django_register` decorator.
    It will not be categorized and will appear in the default admin list.
    """
