# -*- coding: utf-8 -*-
"""
:synopsis: tests for User admin.

.. module: authentication.tests.admin.test_user
.. author: Chris Bartlett <bartlett.christopher.p@gmail.com>
"""
from django.contrib.admin import AdminSite
from django.test import TestCase

from authentication.admin import UserAdmin
from authentication.models import User


class TestUserAdmin(TestCase):
    """ Unit testing of User Admin """

    def test_admin_defaults(self):
        """ Test UserAdmin default construction """
        site = AdminSite()
        admin = UserAdmin(User, site)

        self.assertEqual(
            admin.list_display,
            ('id', 'email', 'first_name', 'last_name',)
        )
        self.assertEqual(admin.list_filter, ())
        self.assertEqual(admin.ordering, ('id',))
        self.assertEqual(
            admin.search_fields,
            ('id', 'email', 'first_name', 'last_name')
        )
        self.assertEqual(
            admin.fieldsets,
            (
                ('Personal info', {
                    'fields': ('email', 'title', 'first_name', 'last_name',)
                }),
                ('Permissions', {
                    'fields': ('is_superuser', 'groups', 'user_permissions')
                }),
            ),
        )
        self.assertEqual(
            admin.add_fieldsets,
            (
                (None, {
                    'fields': (
                        'email', 'title', 'first_name', 'last_name',
                        'password1', 'password2'
                    ),
                }),
            ),
        )
