# Wagtail-bakery

A set of helpers for baking your Django Wagtail site out as flat files.

## Compatibility note

As of July 2022, django-bakery lacks support for Django 4.x. You are advised to use Django 3.2.x (LTS). Alternatively

## Features

* Single management command that will build your Wagtail site out as flat files
* Support for `i18n_patterns`
* Support for generating a static API
* Ready to use Wagtail Buildable views to build all your (un)published pages at once (no extra code required!)

## Installation

```
pip install wagtail-bakery
```

Add `bakery` and `wagtailbakery` to your `INSTALLED_APPS` setting.

```python
INSTALLED_APPS = (
    # ...
    'bakery',
    'wagtailbakery',
)
```

## Configuration

Define whether you want to build multiple sites or the default site (see examples for impact on directory output), by default this settings is `False`.

```python
BAKERY_MULTISITE = True
```

Add the build directory where you want to be the site be built as flat files.

```python
BUILD_DIR = '/tmp/build/'
```

Build all published public pages (use for production).

```python
BAKERY_VIEWS = (
	'wagtailbakery.views.AllPublishedPagesView',
)
```

Build all published and unpublished public pages (use for staging/acceptance).

```python
BAKERY_VIEWS = (
	'wagtailbakery.views.AllPagesView',
)
```

To build static JSON files representing your site's API, use the following views:

```python
BAKERY_VIEWS = (
	'wagtailbakery.api_views.PagesAPIDetailView',
	'wagtailbakery.api_views.PagesAPIListingView',
	'wagtailbakery.api_views.TypedPagesAPIListingView',
)
```

## Usage

Build the site out as flat files by running the `build` management command.

```
manage.py build
```

If you want to check how your static website will look, use the `buildserver` command after you have build your static files once.

```
manage.py buildserver
```

**Build output with `BAKERY_MULTISITE=True`**:

```
build/example.com/index.html
build/example.com/about/index.html
build/example.com/blog/index.html
build/example.com/blog/example/index.html
build/static/
```

**Build output with `BAKERY_MULTISITE=False` (default)**:

```
build/index.html
build/about/index.html
build/blog/index.html
build/blog/example/index.html
build/static/
```

## Supported Versions


### Python/Django/Wagtail support

Python versions as defined in `setup.py` classifiers.

#### Which version combinations to include in Github Actions test matrix?

In order to keep for CI build time from growing out of control, not all Python/Django/Wagtail combinations will be tested.

Test as follow:
- All supported Django/Wagtail combinations with the latest supported Python version.
- The latest supported Django/Wagtail combination for the remaining Python versions.

