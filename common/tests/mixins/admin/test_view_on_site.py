# -*- coding: utf-8 -*-
"""
  :synopsis: unit test suite for view on site.

.. module: common.tests.mixins.admin.test_view_on_site
.. author: Chris Bartlett <chris.bartlett@therealbuzzgroup.com>
"""
from unittest.mock import patch

from django.contrib.admin import AdminSite, ModelAdmin
from django.db import models
from django.test import TestCase
from django.utils.safestring import SafeString

from common.mixins.admin import ViewOnSiteMixin


class TestViewOnSiteMixin(TestCase):
    """Unit test class for view on site mixin."""

    class TestModelViewOnSiteMixin(models.Model):

        class Meta:
            abstract = True

    class TestAdminViewOnSiteMixin(ModelAdmin):
        pass

    def test_view_on_site(self):
        site = AdminSite()
        obj = self.TestModelViewOnSiteMixin()
        mixin = ViewOnSiteMixin(self.TestModelViewOnSiteMixin, site)
        with patch.object(mixin, 'get_view_on_site_url') as mock:
            mock.return_value = 'my-site-url'
            link = mixin.view_on_site(obj)

        self.assertIsInstance(link, SafeString)
        self.assertEqual(
            link,
            "<a href='my-site-url' target='_blank'>View on site</a>"
        )
        mock.assert_called_once_with(obj)
