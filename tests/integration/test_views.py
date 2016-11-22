import pytest

from django.conf import settings
from wagtailbakery.views import AllPublishedPagesView, WagtailBakeryView

from tests.factories.site import SiteFactory


@pytest.mark.django_db
def test_wagtail_bakery_view_get_site(multisite):
    view = WagtailBakeryView()
    site = view.get_site()

    # Check if default site is returned
    assert site.id == multisite[0].id

    # Check if changed default site is returned
    multisite[0].is_default_site = False
    multisite[0].save()
    multisite[1].is_default_site = True
    multisite[1].save()
    site = view.get_site()
    assert site.id == multisite[1].id


@pytest.mark.django_db
def test_wagtail_bakery_view_get_url(page_tree):
    view = WagtailBakeryView()

    # Check url for homepage
    url = view.get_url(page_tree)
    assert url == '/'

    # Check child url for first child page
    child_page = page_tree.get_descendants().first()
    url = view.get_url(child_page)
    assert url == '/first/'

    # Check child url of the first child page
    child_page = child_page.get_descendants().first()
    url = view.get_url(child_page)
    assert url == '/first/first/'


@pytest.mark.django_db
def test_wagtail_bakery_view_build_path(page_tree):
    view = WagtailBakeryView()

    # Check build path for homepage
    build_path = view.get_build_path(page_tree)
    assert build_path == settings.BUILD_DIR + '/index.html'

    # Check child build path for first child page
    child_page = page_tree.get_descendants().first()
    build_path = view.get_build_path(child_page)
    assert build_path == settings.BUILD_DIR + '/first/index.html'

    # Check child build path of the first child page
    child_page = child_page.get_descendants().first()
    build_path = view.get_build_path(child_page)
    assert build_path == settings.BUILD_DIR + '/first/first/index.html'


@pytest.mark.django_db
def test_all_published_pages_for_single_page(page):
    view = AllPublishedPagesView()
    qs = view.get_queryset()

    # Check if published page is returned
    assert qs.filter(id=page.id).exists()

    # Check if there are no unpublished pages returned
    page.live = False
    page.save()
    assert not qs.filter(live=False).exists()
    assert not qs.filter(id=page.id).exists()


@pytest.mark.django_db
def test_all_published_pages_for_multiple_pages(page_tree):
    view = AllPublishedPagesView()
    qs = view.get_queryset()

    # Check if all pages in page tree are returned
    assert qs.count() == 6