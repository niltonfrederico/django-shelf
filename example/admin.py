from django.contrib.admin.decorators import register as django_register

from admin_shelf import admin
from example.models import Model1, Model2, Model3, Model4, Model5

CustomCategory = admin.Category(name="Custom Category", order=2)
OtherCategory = admin.Category(name="Other Category", order=1)


@admin.register(Model1, category=CustomCategory, order=2)
class Model1Admin(admin.ModelAdmin):
    pass


@admin.register(Model2, category=CustomCategory, order=1)
class Model2Admin(admin.ModelAdmin):
    pass


@admin.register(Model3, category=OtherCategory)
class Model3Admin(admin.ModelAdmin):
    """
    We will keep this model without ordering to show that
    the default alphabetical ordering is applied
    when no order is specified.
    """


@django_register(Model4)
class Model4Admin(admin.ModelAdmin):
    """
    This admin is registered using the `@django_register` decorator.
    It will not be categorized and will appear in the default admin list.
    """


@admin.register(Model5, category=OtherCategory)
class Model5Admin(admin.ModelAdmin):
    """
    We will keep this model without ordering to show that
    the default alphabetical ordering is applied
    when no order is specified.
    """
