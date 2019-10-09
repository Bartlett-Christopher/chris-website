# -*- coding: utf-8 -*-
"""
  :synopsis: unit test suite for common utility collect project apps.

.. module: common.tests.utils.test_collect_project_apps
.. author: Chris Bartlett <chris.bartlett@therealbuzzgroup.com>
"""
from unittest.mock import patch

from django.conf import settings
from django.test import TestCase

from common.utils.collect_apps import collect_project_apps


class TestCollectProjectApps(TestCase):
    """Unit test class for utility collect project apps."""

    @classmethod
    def setUpClass(cls):
        super(TestCollectProjectApps, cls).setUpClass()

        class TestProjectApp:
            """Test class for project apps."""

            def __init__(self, name='', path=''):
                super(TestProjectApp, self).__init__()
                self.name = name
                self.path = path

        cls.app_klass = TestProjectApp

    @patch('common.utils.collect_apps.apps.get_app_configs')
    def test_collect_project_apps__no_apps(self, mock_app_configs):
        """Test no project apps returns empty set."""
        mock_app_configs.return_value = []

        apps = collect_project_apps()

        self.assertSetEqual(apps, set())
        self.assertEqual(mock_app_configs.call_count, 1)

    @patch('common.utils.collect_apps.apps.get_app_configs')
    def test_collect_project_apps__apps_not_project_apps(
            self, mock_app_configs):
        """Test apps not in project directory are not returned."""
        app = self.app_klass(name='unknown', path='blah/test.py')
        mock_app_configs.return_value = [app]

        apps = collect_project_apps()

        self.assertSetEqual(apps, set())
        self.assertEqual(mock_app_configs.call_count, 1)

    @patch('common.utils.collect_apps.apps.get_app_configs')
    def test_collect_project_apps__apps_are_project_apps(
            self, mock_app_configs):
        """Test apps not in project directory are returned."""
        app = self.app_klass(
            name='app',
            path=settings.PROJECT_DIR + '/blah/test.py'
        )
        mock_app_configs.return_value = [app]

        apps = collect_project_apps()

        self.assertSetEqual(apps, {app.name})
        self.assertEqual(mock_app_configs.call_count, 1)
