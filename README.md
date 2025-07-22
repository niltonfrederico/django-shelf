[![codecov](https://codecov.io/github/niltonfrederico/django-shelf/branch/main/graph/badge.svg?token=SATSBNDY0B)](https://codecov.io/github/niltonfrederico/django-shelf)
![pip](https://img.shields.io/pypi/v/django-admin-shelf
)

```
 ░▒▓███████▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓████████▓▒░▒▓█▓▒░      ░▒▓████████▓▒░
░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░      ░▒▓█▓▒░
░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░      ░▒▓█▓▒░
 ░▒▓██████▓▒░░▒▓████████▓▒░▒▓██████▓▒░ ░▒▓█▓▒░      ░▒▓██████▓▒░
       ░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░      ░▒▓█▓▒░
       ░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░      ░▒▓█▓▒░
░▒▓███████▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓████████▓▒░▒▓████████▓▒░▒▓█▓▒░
```

## Who?
**Django Shelf** is meant to be a simple way to categorize your model admins instead of relying on creating new apps for each category.

## Bu... but why?
The main reason is simply to avoid creating new apps for each category of model admins. This is especially useful if you got legacy applications that will break if you try to split them into new apps.

Yes, I know that this is not the best practice, but sometimes you just need to do it.

## How do I use it?
1. Install the package using `pip install django-admin-shelf`.
2. Add `admin_shelf` to your `INSTALLED_APPS` in your Django settings.
3. Create categories in your `admin.py` file as follows:

```python
from admin_shelf.admin import Category
from example.models import Model1

custom_category = Category(name="Custom Category")

@custom_category.register(Model1)
class Model1Admin(admin.ModelAdmin):
    pass
```

## A little piece of documentation

The `admin_shelf.admin.Category` class is used to create categories for your model admins. You can register your model admins to these categories using the `@category.register(Model)` decorator.

You can set a order for both the categories and the model admins by passing an `order` argument to the `Category` class and the `@register` decorator, respectively.

Example:

```python
from admin_shelf.admin import Category
from example.models import Model1, Model2

custom_category = Category(name="Custom Category", order=1)

@custom_category.register(Model1, order=2)
class Model1Admin(admin.ModelAdmin):
    pass

@custom_category.register(Model2, order=1)
class Model2Admin(admin.ModelAdmin):
    pass
```

Yes, it is just that simple. You can also use the `@register` decorator without passing a category, in which case it will be registered to the default category. Or use the default `register` from django admin if you want to register your model admin without a category.

## Anything else?

### Running the example app

To run the example app, you can use the following commands:
```bash
# You need to have docker installed
docker compose up example
```

### Running the tests
To run the tests, you can use the following commands:
```bash
# You need to have docker installed
docker compose up test
```

## How do I contribute?
If you want to contribute to this project, you can do so by creating an issue! And if you want to contribute with code, you can fork the repository and create a pull request.

Check the [CONTRIBUTING.md](CONTRIBUTING.md) file for more information on how to contribute.

## Is it true that bananas are radioactive?
Yes.
