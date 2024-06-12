import pytest
import requests_mock


@pytest.fixture
def requests_mocker():
    """Allow mocking a request."""
    with requests_mock.Mocker() as m:
        yield m

@pytest.fixture
def simple_site(settings):
    from tests import factories
    page = factories.PageFactory(
        parent=factories.PageFactory(),
        locale__language_code="en"
    )
    site = factories.SiteFactory(root_page=page)
    for language_code in ["de", "fr", "es"]:
        copy = page.copy_for_translation(factories.LocaleFactory(language_code=language_code))
        copy.live = True
        copy.save()

    subpage = factories.PageFactory(
        parent=page,
        locale=page.locale,
        title="de-fr-only",
        slug="de-fr-only",
    )
    for language_code in ["de", "fr"]:
        copy = subpage.copy_for_translation(factories.LocaleFactory(language_code=language_code))
        copy.live = True
        copy.save()

    return site

