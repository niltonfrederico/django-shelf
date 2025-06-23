from django.contrib import admin

from example.models import First, Second, Third


@admin.register(First)
class FirstAdmin(admin.ModelAdmin):  # type: ignore[type-arg]
    pass


@admin.register(Second)
class SecondAdmin(admin.ModelAdmin):  # type: ignore[type-arg]
    pass


@admin.register(Third)
class ThirdAdmin(admin.ModelAdmin):  # type: ignore[type-arg]
    pass
