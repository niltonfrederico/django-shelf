from django.contrib.admin.decorators import register as django_register

from admin_shelf import admin
from example.models import Model1, Model2, Model3, Model4, Model5

custom_category = admin.Category(name="Custom Category", order=2)
other_category = admin.Category(name="Other Category", order=1)


@custom_category.register(Model1, order=2)
class Model1Admin(admin.ModelAdmin):
    pass


@custom_category.register(Model2, order=1)
class Model2Admin(admin.ModelAdmin):
    pass


@other_category.register(Model3)
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


@other_category.register(Model5)
class Model5Admin(admin.ModelAdmin):
    """
    We will keep this model without ordering to show that
    the default alphabetical ordering is applied
    when no order is specified.
    """
