[![codecov](https://codecov.io/github/niltonfrederico/django-shelf/branch/main/graph/badge.svg?token=SATSBNDY0B)](https://codecov.io/github/niltonfrederico/django-shelf)
![pip](https://img.shields.io/pypi/v/django-admin-shelf)

```
  ____  _                           ____  _          _  __
 |  _ \(_) __ _ _ __   __ _  ___   / ___|| |__   ___| |/ _|
 | | | | |/ _` | '_ \ / _` |/ _ \  \___ \| '_ \ / _ \ | |_
 | |_| | | (_| | | | | (_| | (_) |  ___) | | | |  __/ |  _|
 |____// |\__,_|_| |_|\__, |\___/  |____/|_| |_|\___|_|_|
     |__/             |___/
```

## What's in here?

- [Who?](#who)
- [Bu... but why?](#bu-but-why)
- [How do I use it?](#how-do-i-use-it)
- [A little piece of documentation](#a-little-piece-of-documentation)
- [What can I configure?](#what-can-i-configure)
- [How does it hook into the admin?](#how-does-it-hook-into-the-admin)
- [Translation support](#translation-support)
- [What might trip me up?](#what-might-trip-me-up)
- [Anything else?](#anything-else)
  - [Running the example app](#running-the-example-app)
  - [Running the tests](#running-the-tests)
- [How do I contribute?](#how-do-i-contribute)
- [Is it true that bananas are radioactive?](#is-it-true-that-bananas-are-radioactive)
- [CONTRIBUTING.md](CONTRIBUTING.md)

## Who?

**Django Shelf** is meant to be a simple way to categorize your model admins instead of relying on creating new apps for each category.

## Bu... but why?

The main reason is simply to avoid creating new apps for each category of model admins. This is especially useful if you got legacy applications that will break if you try to split them into new apps.

Yes, I know that this is not the best practice, but sometimes you just need to do it.

## How do I use it?

1. Install the package using `pip install django-admin-shelf`.
1. Add `admin_shelf` to your `INSTALLED_APPS` in your Django settings.
1. Create categories in your `admin.py` file as follows:

```python
from django.contrib import admin

from admin_shelf.admin import Category
from example.models import Model1

custom_category = Category(name="Custom Category")

@custom_category.register(Model1)
class Model1Admin(admin.ModelAdmin):
    pass
```

## A little piece of documentation

The `admin_shelf.admin.Category` class is used to create categories for your model admins. You can register your model admins to these categories using the `@category.register(Model)` decorator.

You can set an order for both the categories and the model admins by passing an `order` argument to the `Category` class and the `@register` decorator, respectively.

Example:

```python
from django.contrib import admin

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

Yes, it is just that simple. Use the default `register` from django admin if you want to register your model admin without a category.

Before shelf:
![Before using admin shelf](https://raw.githubusercontent.com/niltonfrederico/django-shelf/refs/heads/main/docs/assets/before-shelf.png)

After shelf:
![After using admin shelf](https://raw.githubusercontent.com/niltonfrederico/django-shelf/refs/heads/main/docs/assets/after-shelf.png)

## What can I configure?

<!-- TODO: DJANGO_ADMIN_SHELF table (HIDE_CATEGORIZED_MODELS, CATEGORY_DEFAULT_ORDER, MODEL_DEFAULT_ORDER) + paragraph on categorized vs plain coexistence (_categorize_models flow at conceptual level). -->

## How does it hook into the admin?

<!-- TODO: explain that adding admin_shelf to INSTALLED_APPS swaps admin.site.__class__ via apps.py:ready(); cover the custom AdminSite subclass edge case. -->

## Translation support

`Category(name=...)` accepts both plain strings and Django's lazy translation
proxies. To localize a category, pass a `gettext_lazy` value:

```python
from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from admin_shelf.admin import Category
from myapp.models import Product

shop_category = Category(name=_("Shop"))

@shop_category.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass
```

The name is resolved against the active language on every request, so users
switching languages see the category label update accordingly.

**Recommendation:** define each `Category` once and reuse the same instance
across `@register` calls. Buckets are keyed by `name`, so two `Category("Shop")`
end up merged anyway — but sharing one instance keeps intent obvious and makes
a later rename a one-liner.

## What might trip me up?

<!-- TODO: reusing same Category instance across files, slug derivation from name, lazy-slug URL changes per language, ordering ties (stable sort, insertion order wins), apps disappearing when HIDE_CATEGORIZED_MODELS=True and all models are categorized. -->

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
