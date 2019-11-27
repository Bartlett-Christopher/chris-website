# -*- coding: utf-8 -*-
"""
  :synopsis: Unit tests suite for EnquiryView.

.. module: home.tests.views.test_enquiry
.. author: Chris Bartlett <chris.bartlett@therealbuzzgroup.com>
"""
from unittest import mock

from django.test import RequestFactory, TestCase

from home.forms import EnquiryForm
from home.models import Enquiry
from home.views import EnquiryView


class TestEnquiryView(TestCase):
    """Unit test class for EnquiryView."""

    def test_form_valid(self):
        rf = RequestFactory()
        request = rf.get('enquiry/')
        data = {
            'name': 'Chief Tester',
            'email': 'test@testing.com',
            'message': 'hello, world!'
        }
        form = EnquiryForm(data=data)
        enquiry = Enquiry(**data)
        view = EnquiryView(request=request)

        with mock.patch.object(form, 'save') as mock_form_save:
            mock_form_save.return_value = enquiry
            response = view.form_valid(form)

        mock_form_save.assert_called_once_with(commit=True)
        self.assertEqual(response.status_code, 200)
        self.assertListEqual(response.template_name, ['home/enquiry.html'])
        self.assertEqual(response.context_data['enquiry'], enquiry)
        self.assertTrue(response.context_data['request_received'])
