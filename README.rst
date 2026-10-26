=====================================
labdigital-wagtail-localemiddleware
=====================================

A drop-in replacement for Django's ``LocaleMiddleware`` for Wagtail sites that
use ``i18n_patterns(..., prefix_default_language=False)``. With that setup,
Django always serves unprefixed URLs in ``LANGUAGE_CODE`` and never redirects
visitors to their own language. This middleware picks the visitor's language
from the URL prefix, the language cookie or the ``Accept-Language`` header.
If the URL exists with that language prefix, the visitor is redirected to it:
for example, a German browser requesting ``/`` gets a ``302`` to ``/de/``.

Status
======

Early stage: version 0.0.1. It is not published on PyPI yet (see
`Release process`_).

Requirements
============

- Python 3.11 or newer
- Django and Wagtail. CI tests Django 5.2 with Wagtail 7.0 and 8.0, and
  Django 6.0 with Wagtail 8.0.

Installation
============

Once the package is released, install it under the dist name
``labdigital-wagtail-localemiddleware``:

.. code-block:: shell

   pip install labdigital-wagtail-localemiddleware
   # or
   uv add labdigital-wagtail-localemiddleware

Until then, install it from GitHub:

.. code-block:: shell

   pip install git+https://github.com/labd/python-wagtail-localemiddleware.git

The import path is ``labd.middleware.locale``.

Usage
=====

Put ``labd.middleware.locale.LocaleMiddleware`` in ``MIDDLEWARE`` where
Django's ``LocaleMiddleware`` would go: after ``SessionMiddleware`` and before
``CommonMiddleware``. It replaces ``django.middleware.locale.LocaleMiddleware``,
so do not add both.

.. code-block:: python

   # settings.py
   MIDDLEWARE = [
       "django.middleware.security.SecurityMiddleware",
       "django.contrib.sessions.middleware.SessionMiddleware",
       "labd.middleware.locale.LocaleMiddleware",
       "django.middleware.common.CommonMiddleware",
       # ...
   ]

   USE_I18N = True
   WAGTAIL_I18N_ENABLED = True
   LANGUAGE_CODE = "en"
   WAGTAIL_CONTENT_LANGUAGES = LANGUAGES = [
       ("en", "English"),
       ("de", "German"),
       ("fr", "French"),
   ]

Serve the Wagtail page tree through ``i18n_patterns`` without a prefix for the
default language:

.. code-block:: python

   # urls.py
   from django.conf.urls.i18n import i18n_patterns
   from django.urls import include, path
   from wagtail import urls as wagtail_urls
   from wagtail.admin import urls as wagtailadmin_urls

   urlpatterns = [
       path("admin/", include(wagtailadmin_urls)),
   ] + i18n_patterns(
       path("", include(wagtail_urls)),
       prefix_default_language=False,
   )

What changes compared to Django's ``LocaleMiddleware``:

- **Request**: if the detected language differs from the active one and
  ``/<language><path>`` resolves, that language is activated. Otherwise
  Django's normal behaviour applies.
- **Response**: on a ``404`` for an unprefixed path, the visitor is redirected
  to ``/<language><path>`` (adding a trailing slash if ``APPEND_SLASH`` needs
  it). This happens unless the language is ``LANGUAGE_CODE`` or the path
  already has a language prefix. Django itself only does this when
  ``prefix_default_language=True``. The redirect gets ``Vary: Accept-Language``.
- A ``Content-Language`` header is set if the response does not have one yet.

The middleware has no settings of its own.

Development
===========

The project uses `uv <https://docs.astral.sh/uv/>`_. The ``Makefile`` wraps
the common commands:

.. code-block:: shell

   make install    # uv sync
   make test       # uv run pytest
   make coverage   # pytest with coverage report
   make format     # ruff format + ruff check --fix
   make lint       # ruff format --check + ruff check

CI (``.github/workflows/python-package.yaml``) checks formatting with ruff and
runs the test matrix through tox:

.. code-block:: shell

   uvx --with tox-uv tox -e py313-django52-wagtail80

The tests set up Django in ``tests/conftest.py`` with an SQLite database, so
nothing else needs to run.

Release process
===============

1. Bump ``version`` in ``pyproject.toml`` and add an entry to ``CHANGES``.
2. Create a GitHub release. The ``Release to PyPi`` workflow
   (``.github/workflows/python-release.yaml``) builds the package with
   ``uv build`` and publishes it to PyPI with trusted publishing (OIDC). No API
   token is needed.

License
=======

MIT, see `LICENSE <LICENSE>`_.
