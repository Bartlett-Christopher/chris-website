# -*- coding: utf-8 -*-
"""
  :synopsis: unit test suite for Page model.

.. module: staticpages.tests.models.test_page
.. author: Chris Bartlett <chris.bartlett@therealbuzzgroup.com>
"""
from unittest.mock import patch

from django.db.models.signals import pre_save
from django.test import TestCase
from django_dynamic_fixture import G

from staticpages.exceptions import PageNotFound
from staticpages.models.page import Page, pre_save_static_page


class TestPage(TestCase):
    """Unit test class for Page model."""

    @classmethod
    def setUpClass(cls):
        super(TestPage, cls).setUpClass()
        pre_save.disconnect(
            receiver=pre_save_static_page,
            sender=Page
        )

    @classmethod
    def tearDownClass(cls):
        pre_save.connect(
            receiver=pre_save_static_page,
            sender=Page
        )
        super(TestPage, cls).tearDownClass()

    def test_get_page__page_does_not_exist(self):
        """Test no page found raises error."""
        url = '/unknown-page/'

        with patch.object(Page, 'process_url') as mock_process:
            mock_process.return_value = url
            with self.assertRaises(PageNotFound):
                Page.get_page(url)

        self.assertEqual(mock_process.call_count, 1)

    def test_get_page__page_found(self):
        """Test page found is returned."""
        url = '/page-exists/'
        page = G(Page, url=url, fill_nullable_fields=False)

        found_page = Page.get_page(url=url)

        self.assertEqual(page, found_page)

    def test_process_url__append_slash_to_start(self):
        """Test url has start slash added."""
        url = Page.process_url('no-start/')

        self.assertEqual(url, '/no-start/')

    def test_process_url__append_slash_to_end(self):
        """Test url has final slash added."""
        url = Page.process_url('/no-end')

        self.assertEqual(url, '/no-end/')

    def test_process_url__no_changes_required(self):
        """Test valid url is unchanged."""
        url = '/valid-url/'

        final_url = Page.process_url(url)

        self.assertEqual(url, final_url)

    def test_process_url__middle_slashes_unchanged(self):
        """Test slahsed in middle url not modified."""
        url = '/valid/url/'

        final_url = Page.process_url(url)

        self.assertEqual(url, final_url)

    def test_pre_save_signal__has_template_name(self):
        """Test instance template name unchanged."""
        template_name = 'staticpages/custom-template/html'
        instance = Page(
            url='/has-template/',
            template_name=template_name
        )

        with patch.object(Page, 'process_url') as mock_process:
            mock_process.return_value = instance.url
            pre_save_static_page(sender=Page, instance=instance)

        self.assertEqual(instance.template_name, template_name)
        mock_process.assert_called_once_with(instance.url)

    def test_pre_save_signal__no_template_name_one_added(self):
        """Test default template name added to instance if None."""
        instance = Page(
            url='/no-template/',
        )

        with patch.object(Page, 'process_url') as mock_process:
            mock_process.return_value = instance.url
            pre_save_static_page(sender=Page, instance=instance)

        self.assertEqual(instance.template_name, 'staticpages/page.html')
        mock_process.assert_called_once_with(instance.url)
