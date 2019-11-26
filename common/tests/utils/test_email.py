# -*- coding: utf-8 -*-
"""
  :synopsis: Unit test module for sending email.

.. module: common.tests.utils.test_email
.. author: Chris Bartlett <chris.bartlett@therealbuzzgroup.com>
"""
import json

from background_task.models import Task
from unittest import mock

from django.conf import settings
from django.test import TestCase, override_settings

from common.utils.email import send_email


class TestSendEmail(TestCase):
    """Test class for common utility send_email."""

    def setUp(self):
        super(TestSendEmail, self).setUp()
        Task.objects.all().delete()

    @override_settings(EMAIL_DEBUG=True)
    @mock.patch('common.utils.email.django_send_mail')
    def test_send_email__debug_mode(self, mock_django_mail):
        func_kwargs = {
            'recipient': ['test@gmail.com'],
            'subject': 'Test Debug email sending',
            'text': 'hello, world'
        }
        send_email(**func_kwargs)

        # assert task object created
        task = Task.objects.last()
        self.assertEqual(task.task_name, 'common.utils.email.send_email')
        self.assertEqual(
            task.task_params,
            json.dumps(
                [
                    [],
                    {
                        'recipient': ['test@gmail.com'],
                        'subject': 'Test Debug email sending',
                        'text': 'hello, world'
                    }
                ]
            )
        )
        self.assertEqual(task.queue, 'email')

        # assert running task executes function correctly
        send_email.task_function(**func_kwargs)

        self.assertEqual(mock_django_mail.call_count, 0)

    @override_settings(EMAIL_DEBUG=False)
    @mock.patch('common.utils.email.django_send_mail')
    def test_send_email__production_mode(self, mock_django_mail):
        func_kwargs = {
            'recipient': 'test@gmail.com',
            'subject': 'Test Debug email sending',
            'text': 'hello, world'
        }
        send_email(**func_kwargs)

        # assert task object created
        task = Task.objects.last()
        self.assertEqual(task.task_name, 'common.utils.email.send_email')
        self.assertEqual(
            task.task_params,
            json.dumps(
                [
                    [],
                    {
                        'recipient': 'test@gmail.com',
                        'subject': 'Test Debug email sending',
                        'text': 'hello, world'
                    }
                ]
            )
        )
        self.assertEqual(task.queue, 'email')

        # assert running task executes function correctly
        send_email.task_function(**func_kwargs)

        mock_django_mail.assert_called_once_with(
            subject='Test Debug email sending',
            message='hello, world',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=['test@gmail.com'],
            fail_silently=False,
            html_message=None
        )
