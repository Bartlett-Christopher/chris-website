# -*- coding: utf-8 -*-
"""
  :synopsis: Unit test suite for staticpage Page admin.

.. module: staticpages.tests.admin.test_page
.. author: Chris Bartlett <chris.bartlett@therealbuzzgroup.com>
"""
from unittest.mock import Mock, patch

from django.contrib import admin
from django.test import TestCase
from django.utils.safestring import SafeString

from staticpages.admin.page import PageAdmin
from staticpages.models.page import Page


class TestPageAdmin(TestCase):
    """Unit test class for Page admin."""

    @classmethod
    def setUpClass(cls):
        super(TestPageAdmin, cls).setUpClass()
        cls.admin = PageAdmin(Page, admin.site)

    def test_view_on_site(self):
        obj = object()
        with patch.object(self.admin, 'get_view_on_site_url') as mock:
            mock.return_value = 'static-page-1'
            link = self.admin.view_on_site(obj)

        self.assertIsInstance(link, SafeString)
        self.assertEqual(
            link,
            "<a href='static-page-1' target='_blank'>View on site</a>"
        )
        mock.assert_called_once_with(obj)

    def test_get_view_on_site_url__no_obj(self):
        self.assertIsNone(self.admin.get_view_on_site_url(None))

    def test_get_view_on_site_url__has_obj(self):
        obj = Mock(**{'url': 'static-page-1'})
        self.assertEqual(self.admin.get_view_on_site_url(obj), 'static-page-1')
