from django.conf import settings

pytest_plugins = "tests.fixtures"

WAGTAIL_CONTENT_LANGUAGES = LANGUAGES = [
    ("en", "English"),
    ("de", "German"),
    ("fr", "French"),
    ("es", "Spanish"),
]


def pytest_configure():
    settings.configure(
        ROOT_URLCONF="tests.urls",
        MIDDLEWARE=[
            "django.middleware.security.SecurityMiddleware",
            "django.contrib.sessions.middleware.SessionMiddleware",
            "labd.middleware.locale.LocaleMiddleware",
            "django.middleware.common.CommonMiddleware",
            "django.middleware.csrf.CsrfViewMiddleware",
            "django.contrib.auth.middleware.AuthenticationMiddleware",
            "django.contrib.messages.middleware.MessageMiddleware",
            "django.middleware.clickjacking.XFrameOptionsMiddleware",
        ],
        STATIC_URL="/static/",
        USE_I18N=True,
        WAGTAIL_I18N_ENABLED=True,
        LANGUAGE_CODE="en",
        WAGTAIL_CONTENT_LANGUAGES=WAGTAIL_CONTENT_LANGUAGES,
        LANGUAGES=LANGUAGES,
        INSTALLED_APPS=[
            "wagtail.contrib.forms",
            "wagtail.contrib.redirects",
            "wagtail.embeds",
            "wagtail.sites",
            "wagtail.users",
            "wagtail.snippets",
            "wagtail.documents",
            "wagtail.images",
            "wagtail.search",
            "wagtail.admin",
            "wagtail",
            "modelcluster",
            "taggit",
            "django.contrib.admin",
            "django.contrib.auth",
            "django.contrib.contenttypes",
            "django.contrib.sessions",
            "django.contrib.messages",
            "django.contrib.staticfiles",
        ],
        SECRET_KEY="potato",
        TEMPLATES=[
            {
                "BACKEND": "django.template.backends.django.DjangoTemplates",
                "DIRS": [],
                "APP_DIRS": True,
                "OPTIONS": {
                    "context_processors": [
                        "django.template.context_processors.debug",
                        "django.template.context_processors.request",
                        "django.contrib.auth.context_processors.auth",
                        "django.contrib.messages.context_processors.messages",
                    ]
                },
            }
        ],
        CACHES={
            "default": {
                "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
                "LOCATION": "unique-snowflake",
            }
        },
        DATABASES={"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": "db.sqlite"}},
    )
