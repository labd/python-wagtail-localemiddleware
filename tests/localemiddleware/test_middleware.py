import pytest


from django.test import Client


@pytest.mark.parametrize(
    "accept_language,status_code,location",
    (
        ("en", 200, None),
        ("de", 302, "/de/"),
        ("fr", 302, "/fr/"),
        ("es", 302, "/es/"),
    )
)
@pytest.mark.django_db
def test_middleware(simple_site, settings, accept_language, status_code,
                    location):
    page = simple_site.root_page
    assert page.get_translations().live().count() == 3
    assert {x.url for x in page.get_translations().live()} == {'/es/', '/fr/', '/de/'}

    subpage = page.get_children().live().first()
    assert subpage.get_translations().live().count() == 2

    client = Client(HTTP_ACCEPT_LANGUAGE=accept_language)
    response = client.get("/")
    assert response.status_code == status_code
    assert response.get("location") == location
