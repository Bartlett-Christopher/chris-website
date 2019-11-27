# -*- coding: utf-8 -*-
"""
  :synopsis: Unit tests for enquiry admin

.. module: home.tests.admin.test_enquiry
.. author: Chris Bartlett <chris.bartlett@therealbuzzgroup.com>
"""
from unittest import mock

from django.contrib.admin import site
from django.test import RequestFactory, TestCase
from django_dynamic_fixture import G

from home.admin import EnquiryAdmin
from home.models import Enquiry


class TestEnquiryAdmin(TestCase):
    """Unit tests class for EnquiryAdmin."""

    def test_resolve_enquiries(self):
        rf = RequestFactory()
        request = rf.get('/admin')
        enquiry_resolved = G(
            Enquiry,
            resolved=True,
            fill_nullable_fields=False
        )
        enquiry_outstanding = G(
            Enquiry,
            resolved=False,
            fill_nullable_fields=False
        )
        qs = Enquiry.objects.all()

        admin = EnquiryAdmin(Enquiry, site)

        with mock.patch.object(admin, 'message_user') as mock_msg:
            admin.resolve_enquiries(request, qs)

        enquiry_resolved.refresh_from_db()
        self.assertTrue(enquiry_resolved.resolved)
        enquiry_outstanding.refresh_from_db()
        self.assertTrue(enquiry_outstanding.resolved)
        mock_msg.assert_called_once_with(
            request,
            'Successfully resolved 1 enquiry.'
        )
