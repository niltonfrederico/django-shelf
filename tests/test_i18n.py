from pathlib import Path

from django.test import SimpleTestCase, override_settings
from django.utils import translation
from django.utils.translation import gettext_lazy as _

from admin_shelf.admin import Category

LOCALE_PATH = Path(__file__).parent / "locale"


@override_settings(LOCALE_PATHS=[str(LOCALE_PATH)], USE_I18N=True)
class TestI18nIntegration(SimpleTestCase):
    def test_should_preserve_lazy_proxy_when_constructed_with_gettext_lazy(self):
        lazy_name = _("Shop")

        category = Category(name=lazy_name)

        assert category.name is lazy_name

    def test_should_render_translated_when_language_is_activated(self):
        category = Category(name=_("Shop"))

        with translation.override("pt-br"):
            assert str(category.name) == "Loja"

        with translation.override("en-us"):
            assert str(category.name) == "Shop"

    def test_should_accept_plain_string_alongside_lazy(self):
        plain = Category(name="Operations")
        lazy = Category(name=_("Shop"))

        with translation.override("pt-br"):
            assert str(plain.name) == "Operations"
            assert str(lazy.name) == "Loja"
