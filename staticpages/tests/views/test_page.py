# -*- coding: utf-8 -*-
"""
  :synopsis: unit test suite for staticpages Page view.

.. module: staticpages.test.views.test_page
.. author: Chris Bartlett <chris.bartlett@therealbuzzgroup.com>
"""
from unittest.mock import patch

from django.http import HttpResponse, HttpResponseNotAllowed
from django.test import RequestFactory, TestCase
from django_dynamic_fixture import G

from staticpages.exceptions import PageNotFound
from staticpages.models.page import Page
from staticpages.views.page import PageView


class TestPageView(TestCase):
    """Unit test class for PageView."""

    @classmethod
    def setUpClass(cls):
        super(TestPageView, cls).setUpClass()
        cls.default_page = G(
            Page,
            url='/page-removed/',
            title='Default Page',
            template_name='staticpages/page.html',
            enabled=True,
            fill_nullable_fields=False
        )
        cls.rf = RequestFactory()

    def setUp(self):
        super(TestPageView, self).setUp()
        self.view = PageView()

    def test_init(self):
        """Test class initialisation."""
        self.assertIsNone(self.view.page)

    def test_dispatch__no_url_raises_error(self):
        """Test no url in kwargs raises PageNotFound."""
        request = self.rf.get('/')

        with self.assertRaises(PageNotFound):
            self.view.dispatch(request)

    def test_dispatch__page_disabled_returns_default_page(self):
        """Test disabled page returns page removed page."""
        url = '/disabled-page/'
        G(
            Page,
            url=url,
            enabled=False,
            fill_nullable_fields=False
        )
        request = self.rf.get('/')

        with patch.object(self.view, 'get') as mock_get:
            self.view.dispatch(request, url=url)

        mock_get.assert_called_once_with(request, url=url)
        self.assertEqual(self.view.page, self.default_page)

    def test_dispatch__post_method_not_allowed(self):
        """Test PageView post method not allowed."""
        request = self.rf.post('/', data={})

        response = self.view.dispatch(request, url='/page-removed/')

        self.assertIsInstance(response, HttpResponseNotAllowed)

    def test_get_context(self):
        """Test page in context."""
        self.view.page = self.default_page
        self.assertDictEqual(
            self.view.get_context(),
            {
                'page': self.default_page
            }
        )

    def test_get(self):
        """Test view get method returns HttpResponse."""
        request = self.rf.get('/', url='/page-removed/')
        self.view.page = self.default_page

        with patch.object(self.view, 'get_context') as mock_context:
            mock_context.return_value = {'page': self.default_page}
            response = self.view.get(request)

        self.assertIsInstance(response, HttpResponse)
        self.assertEqual(response.status_code, 200)
        self.assertInHTML(
            f'<h1>{self.default_page.title}</h1>',
            str(response.content)
        )
