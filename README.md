<table align="center">
<tr><td><pre>
  ____  _                           ____  _          _  __
 |  _ \(_) __ _ _ __   __ _  ___   / ___|| |__   ___| |/ _|
 | | | | |/ _` | '_ \ / _` |/ _ \  \___ \| '_ \ / _ \ | |_
 | |_| | | (_| | | | | (_| | (_) |  ___) | | | |  __/ |  _|
 |____// |\__,_|_| |_|\__, |\___/  |____/|_| |_|\___|_|_|
     |__/             |___/
</pre></td></tr>
<tr><td align="center">
<a href="https://codecov.io/github/niltonfrederico/django-shelf"><img src="https://codecov.io/github/niltonfrederico/django-shelf/branch/main/graph/badge.svg?token=SATSBNDY0B" alt="codecov"/></a>
<img src="https://img.shields.io/pypi/v/django-admin-shelf" alt="pip"/>
</td></tr>
</table>

## What's in here?

- [What's in here?](#whats-in-here)
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

### What can I configure?

Settings live under `DJANGO_ADMIN_SHELF` in your Django settings, as a dict. All keys are optional — the defaults are sane.

```python
DJANGO_ADMIN_SHELF = {
    "HIDE_CATEGORIZED_MODELS": True,
    "CATEGORY_DEFAULT_ORDER": 0,
    "MODEL_DEFAULT_ORDER": 0,
}
```

| Key                       | Default | What it does                                                                                                                                     |
| ------------------------- | ------- | ------------------------------------------------------------------------------------------------------------------------------------------------ |
| `HIDE_CATEGORIZED_MODELS` | `True`  | When `True`, a categorized model only shows up inside its category. When `False`, it shows up in both the category and its original app section. |
| `CATEGORY_DEFAULT_ORDER`  | `0`     | Order used when a `Category` is created without an explicit `order`.                                                                             |
| `MODEL_DEFAULT_ORDER`     | `0`     | Order used when a model is registered without an explicit `order`.                                                                               |

Under the hood, when Django builds its admin app list this library walks each app's models. If a model was registered through `@category.register(...)`, it gets moved (or copied, depending on `HIDE_CATEGORIZED_MODELS`) into a bucket named after the category. Categories are then sorted by `order`, and so are the models inside each category.

If `HIDE_CATEGORIZED_MODELS` is `True` and **every** model in an app ends up categorized, the original app section just disappears from the sidebar — there is nothing left to show.

### How does it hook into the admin?

You don't need to touch `admin.site` yourself. As soon as `admin_shelf` is in `INSTALLED_APPS`, the app's `ready()` hook mutates `admin.site.__class__` to `CategorizedAdminSite`. The singleton stays the same — only its class changes — so anything you had already wired to `admin.site` keeps working.

If you maintain your **own** `AdminSite` subclass, that mutation will overwrite it. In that case, inherit from `CategorizedAdminSite` directly:

```python
from admin_shelf.admin import CategorizedAdminSite

class MyAdminSite(CategorizedAdminSite):
    site_header = "My project"
```

### Translation support

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

### What might trip me up?

A few edges worth knowing about:

- **One `Category` per name, please.** Buckets are keyed by `category.name`, so multiple `Category("Shop")` instances merge into the same bucket. It works, but defining each category once and importing it from a single module keeps intent obvious and saves you from chasing duplicates when you want to rename.

- **Category URLs come from the slug of the name.** `Category(name="Custom Category")` lives at `/admin/custom-category/`. The slug is computed from `str(name)` at request time, so it always reflects the current value of the name.

- **Lazy names change URLs per language.** With `Category(name=_("Shop"))`, the URL gets translated too — `/admin/shop/` in English, `/admin/loja/` in Portuguese. Bookmarks and external links pointing at the old slug will 404 after a language switch. If you need a stable URL across languages, use a plain string `name`. ([#27](https://github.com/niltonfrederico/django-shelf/issues/27) tracks a config knob to make this opt-in.)

- **Order ties keep insertion order.** Sorting is stable. Two categories with the same `order` (including the default `0`) appear in the order they were first registered. Non-categorized apps also count as `0`, so they interleave with categorized ones unless you bump categories above `0`. ([#28](https://github.com/niltonfrederico/django-shelf/issues/28) tracks a configurable sub-sort — alphabetical or custom callable — to break ties.)

- **Apps can disappear.** With `HIDE_CATEGORIZED_MODELS=True` (default), if every model in an app gets moved into categories, the original app section vanishes from the sidebar. Intentional — there is nothing left to show — but it can surprise you when a familiar group "disappears" after a refactor.

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

[Yes](https://www.epa.gov/radtown/natural-radioactivity-food).
