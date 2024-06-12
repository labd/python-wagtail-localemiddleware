import factory
import wagtail_factories
from wagtail.models import Locale


class LocaleFactory(factory.django.DjangoModelFactory):
    language_code = "en"

    class Meta:
        model = Locale
        django_get_or_create = ["language_code"]


class PageFactory(wagtail_factories.PageFactory):
    locale = factory.SubFactory(LocaleFactory)


class SiteFactory(wagtail_factories.SiteFactory):
    root_page = factory.SubFactory(PageFactory, parent=None)
    is_default_site = True
