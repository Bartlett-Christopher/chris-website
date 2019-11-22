# -*- coding: utf-8 -*-
"""
  :synopsis: Unit test module for common cron tasks.

.. module: common.tests.test_cron
.. author: Chris Bartlett <chris.bartlett@therealbuzzgroup.com>
"""
from background_task.models import Task
from unittest import mock

from django.test import TestCase
from django_dynamic_fixture import G

from common.cron import process_background_tasks, TASKS


class TestProcessBackgroundTasks(TestCase):
    """Test class for process_background_tasks."""

    @mock.patch('common.cron.task_manager')
    def test_process_background_tasks__no_pending_tasks(
            self, mock_task_manager):
        process_background_tasks()

        self.assertEqual(mock_task_manager.run_task.call_count, 0)

    @mock.patch('common.cron.task_manager')
    def test_process_background_tasks__pending_email_tasks(
            self, mock_task_manager):
        task = G(Task, task_name=TASKS['email'], fill_nullable_fields=False)

        process_background_tasks()

        mock_task_manager.run_task.assert_called_once_with(task)
