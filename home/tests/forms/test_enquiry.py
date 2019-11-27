# -*- coding: utf-8 -*-
"""
  :synopsis: Unit test suite for EnquiryForm.

.. module: home.tests.forms.test_enquiry
.. author: Chris Bartlett <chris.bartlett@therealbuzzgroup.com>
"""
from unittest import mock

from django.conf import settings
from django.template import loader
from django.test import TestCase

from home.forms import EnquiryForm
from home.models import Enquiry


class TestEnquiryForm(TestCase):
    """Unit test class for EnquiryForm."""

    @mock.patch('home.forms.enquiry.send_email')
    def test_save(self, mock_send):
        form = EnquiryForm(
            data={
                'name': 'Chief Tester',
                'email': 'test@testing.com',
                'message': 'hello, world!'
            }
        )

        self.assertTrue(form.is_valid())
        instance = form.save(commit=False)
        self.assertIsInstance(instance, Enquiry)
        self.assertEqual(instance.name, 'Chief Tester')
        self.assertEqual(instance.email, 'test@testing.com')
        self.assertEqual(instance.message, 'hello, world!')
        self.assertFalse(instance.resolved)
        template = loader.get_template('home/email/enquiry.html')
        mock_send.assert_called_once_with(
            recipient=[settings.EMAIL_RECIPIENT],
            subject='Enquiry submitted.',
            text=f"Name: Chief Tester\n"
                 f"Email: test@testing.com\n"
                 f"Message: hello, world!\n",
            html=template.render({'instance': instance})
        )
