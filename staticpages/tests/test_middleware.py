# -*- coding: utf-8 -*-
"""
  :synopsis: unit tests for staticpages middleware.

.. module:: staticpages.tests.test_middleware
.. moduleauthor:: Chris Bartlett <chris.bartlett@therealbuzzgroup.com>
"""
from unittest.mock import create_autospec, patch

from django.http import HttpResponse, HttpResponseNotFound
from django.test import RequestFactory, TestCase
from django.urls import reverse
from django_dynamic_fixture import G
from django_webtest import WebTest

from staticpages.exceptions import PageNotFound
from staticpages.middleware import StaticPageCaptureMiddleware
from staticpages.models.page import Page
from staticpages.views.page import PageView


class TestStaticPageCaptureMiddleware(TestCase):
    """Test class for StaticPageCaptureMiddleware."""

    @classmethod
    def setUpClass(cls):
        super(TestStaticPageCaptureMiddleware, cls).setUpClass()
        cls.rf = RequestFactory()
        cls.request = cls.rf.get('/static-page/')
        cls.standard_response = HttpResponse(content='standard')
        cls.not_found_response = HttpResponseNotFound(content='not found')
        cls.static_page_response = HttpResponse(content='static-page''')
        cls.middleware = StaticPageCaptureMiddleware(
            get_response=lambda: cls.standard_response
        )

    def test_process_response__response_200(self):
        """Test 200 response falls through."""
        processed_response = self.middleware.process_response(
            self.request, self.standard_response
        )

        self.assertEqual(processed_response, self.standard_response)

    @patch('staticpages.middleware.PageView')
    def test_process_response__response_404_no_static_page(self, mock_view):
        """Test 404 response raised is no static page."""
        view = create_autospec(PageView)
        view.dispatch.side_effect = PageNotFound
        mock_view.return_value = view

        processed_response = self.middleware.process_response(
            self.request, self.not_found_response
        )

        self.assertEqual(processed_response, self.not_found_response)
        mock_view.assert_called_once()
        view.dispatch.assert_called_once_with(
            self.request,
            url=self.request.path_info
        )

    @patch('staticpages.middleware.PageView')
    def test_process_response__response_404_static_page_found(self, mock_view):
        """Test static page found and returned after 404."""
        view = create_autospec(PageView)
        view.dispatch.return_value = self.static_page_response
        mock_view.return_value = view

        processed_response = self.middleware.process_response(
            self.request, self.not_found_response
        )

        self.assertEqual(processed_response, self.static_page_response)
        mock_view.assert_called_once()
        view.dispatch.assert_called_once_with(
            self.request,
            url=self.request.path_info
        )


class TestIntegrationStaticPageCaptureMiddleware(WebTest):
    """Webtest class for StaticPageCaptureMiddleware."""

    @classmethod
    def setUpClass(cls):
        super(TestIntegrationStaticPageCaptureMiddleware, cls).setUpClass()
        cls.default_page = G(
            Page,
            url='page-removed',
            title='Page removed',
            fill_nullable_fields=False
        )

    def test_response_200(self):
        """Test 200 response falls through."""
        home = reverse('home:landing')

        response = self.app.get(home)

        self.assertEqual(response.status_code, 200)

    def test_response_404_no_static_page(self):
        """Test 404 response raised when no static page."""
        url = '/definitely-does-not-exist/'

        response = self.app.get(url, status=404)

        self.assertEqual(response.status_code, 404)
        self.assertIn(
            'Page not found',
            response.html.text
        )

    def test_response_404_static_page_found_disabled(self):
        """Test 404 response when static page is disabled."""
        static_page = G(
            Page,
            url='static-page',
            title='Static Page',
            enabled=False,
            fill_nullable_fields=False
        )

        response = self.app.get(static_page.url)

        self.assertEqual(response.status_code, 200)
        self.assertIn(
            'Page removed',
            response.html.text
        )

    def test_response_404_static_page_found_enabled(self):
        """Test static page returned when enabled."""
        static_page = G(
            Page,
            url='static-page',
            title='Static page',
            enabled=True,
            fill_nullable_fields=False
        )

        response = self.app.get(static_page.url)

        self.assertEqual(response.status_code, 200)
        self.assertIn(
            'Static page',
            response.html.text
        )
