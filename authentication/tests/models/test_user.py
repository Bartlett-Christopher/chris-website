# -*- coding: utf-8 -*-
"""
:synopsis: tests for User model.

.. module: authentication.tests.models.user
.. author: Chris Bartlett <bartlett.christopher.p@gmail.com>
"""
from django.test import TestCase

from authentication.models import User


class TestUser(TestCase):
    """ Unit testing of authentication.User """

    def test_str(self):
        """ Test str representation of User """
        user = User(
            title='Dr',
            first_name='Chris',
            last_name='Bartlett',
            email='bartlett.christopher.p@gmail.com',
        )
        self.assertEqual(
            user.__str__(),
            'Dr Chris Bartlett (bartlett.christopher.p@gmail.com)'
        )

    def test_name_1(self):
        """ Test name property no parts """
        user = User()
        self.assertEqual(user.name, '')

    def test_name_2(self):
        """ Test name property - first name only """
        user = User(first_name='Chris')
        self.assertEqual(user.name, 'Chris')

    def test_name_3(self):
        """ Test name property - first and last name """
        user = User(first_name='Chris', last_name='Bartlett')
        self.assertEqual(user.name, 'Chris Bartlett')

    def test_name_4(self):
        """ Test name property - honorific, first and last name """
        user = User(title='Dr', first_name='Chris', last_name='Bartlett')
        self.assertEqual(user.name, 'Dr Chris Bartlett')

    def test_is_staff_1(self):
        """ Test is_staff property - non-superuser """
        user = User(is_superuser=False)
        self.assertFalse(user.is_superuser)
        self.assertFalse(user.is_staff)

    def test_is_staff_2(self):
        """ Test is_staff property - superuser """
        user = User(is_superuser=True)
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
