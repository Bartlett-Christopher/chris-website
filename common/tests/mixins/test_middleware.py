# -*- coding: utf-8 -*-
"""
  :synopsis: unit test suite for common middleware mixin.

.. module: comms.tests.mixins.test_middleware
.. author: Chris Bartlett <chris.bartlett@therealbuzzgroup.com>
"""
from unittest.mock import Mock

from django.http import HttpResponse, HttpResponseRedirect
from django.test import RequestFactory, TestCase

from common.mixins.middleware import MiddlewareMixin


class TestMiddlewareMixin(TestCase):
    """Unit test class for MiddlewareMixin."""

    @classmethod
    def setUpClass(cls):
        super(TestMiddlewareMixin, cls).setUpClass()
        cls.rf = RequestFactory()
        cls.request = cls.rf.get('/')

        class TestMiddlewareMixinClass(MiddlewareMixin):
            """Middleware class for test cases."""

        cls.middleware_klass = TestMiddlewareMixinClass

    def test_init__construction(self):
        """Test mixin constructions saves get_response method."""
        get_response = Mock()

        middleware = self.middleware_klass(get_response)

        self.assertEqual(middleware.get_response, get_response)

    def test_call__no_process_request_no_process_response(self):
        """Test mixin no action taken."""
        get_response = Mock(return_value=HttpResponse())
        middleware = self.middleware_klass(get_response)

        response = middleware(self.request)

        self.assertIsInstance(response, HttpResponse)
        get_response.assert_called_once_with(self.request)

    def test_call__has_process_request(self):
        """Test mixin calls process request."""
        returned_response = HttpResponseRedirect(
            redirect_to='process-request'
        )

        class ProcessRequestClass(MiddlewareMixin):

            @staticmethod
            def process_request(request):
                if request:
                    return returned_response

        get_response = Mock(return_value=HttpResponse())
        middleware = ProcessRequestClass(get_response)

        response = middleware(self.request)

        self.assertIsInstance(response, HttpResponseRedirect)
        self.assertEqual(get_response.call_count, 0)

    def test_call__has_process_response(self):
        """Test mixin calls process response."""
        returned_response = HttpResponseRedirect(
            redirect_to='process-response'
        )

        class ProcessResponseClass(MiddlewareMixin):

            @staticmethod
            def process_response(request, response):
                if request and isinstance(response, HttpResponse):
                    return returned_response

        get_response = Mock(return_value=HttpResponse())
        middleware = ProcessResponseClass(get_response)

        output = middleware(self.request)

        self.assertIsInstance(output, HttpResponseRedirect)
        get_response.assert_called_once_with(self.request)
