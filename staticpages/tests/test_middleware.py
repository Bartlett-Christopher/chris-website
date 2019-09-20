# -*- coding: utf-8 -*-
"""
.. module:: staticpages.tests.test_middleware
   :synopsis: unit tests for staticpages middleware

.. moduleauthor:: Chris Bartlett <chris.bartlett@therealbuzzgroup.com>
"""
from unittest import We
from unittest.mock import create_autospec, patch

from django.http import HttpResponse, HttpResponseNotFound
from django.test import RequestFactory, TestCase

from staticpages.exceptions import PageNotFound
from staticpages.middleware import StaticPageCaptureMiddleware
from staticpages.views.page import PageView


class TestStaticPageCaptureMiddleware(TestCase):
    """ Test class for StaticPageCaptureMiddleware """

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
        processed_response = self.middleware.process_response(
            self.request, self.standard_response
        )

        self.assertEqual(processed_response, self.standard_response)

    @patch('staticpages.middleware.PageView')
    def test_process_response__response_404_no_static_page(self, mock_view):
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
