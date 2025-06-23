from django.contrib import admin

from django_shelf.admin import categorized
from example.models import First, Second, Third


@categorized("Custom Category")
@admin.register(First)
class FirstAdmin(admin.ModelAdmin):  # type: ignore[type-arg]
    pass


@categorized("Custom Category", order=1)
@admin.register(Second)
# @categorized("Custom Category", order=3)
class SecondAdmin(admin.ModelAdmin):  # type: ignore[type-arg]
    pass


@categorized("Another Category")
@admin.register(Third)
# @categorized("Custom Category", order=1)
class ThirdAdmin(admin.ModelAdmin):  # type: ignore[type-arg]
    pass
