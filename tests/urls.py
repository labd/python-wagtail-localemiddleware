from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import include, path
from multilanguage.search import views as search_views
from wagtail import urls as wagtail_urls
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.documents import urls as wagtaildocs_urls

urlpatterns = [
    path("django-admin/", admin.site.urls),
    path("admin/", include(wagtailadmin_urls)),
    path("documents/", include(wagtaildocs_urls)),
]

urlpatterns = urlpatterns + i18n_patterns(
    path("search/", search_views.search, name="search"),
    path("", include(wagtail_urls)),
    prefix_default_language=False,
)
