# -*- coding: utf-8 -*-
"""
.. module: authentication.tests.test_manager
  :synopsis: Unit tests for User Manager

.. moduleauthor:: Chris Bartlett <bartlett.christopher.p@gmail.com>
"""
from django.test import TestCase
from django_dynamic_fixture import G

from authentication.manager import UserManager
from authentication.models import User


class TestUserManager(TestCase):
    """ Unit tests for UserManager """

    @classmethod
    def setUpClass(cls):
        super(TestUserManager, cls).setUpClass()
        cls.email = 'testing@gmail.com'
        cls.password = 'Password1!'

    def tearDown(self):
        User.objects.all().delete()

    def test_get_by_email(self):
        """ Test get_by_email utility method """
        user = G(User, email=self.email)
        self.assertEqual(
            User.objects.get_by_email(email=self.email),
            user
        )

    def test__create_user_1(self):
        """ Test no email given raises ValueError """
        with self.assertRaisesMessage(ValueError, 'Email must be set'):
            User.objects._create_user(email='', password='', is_superuser=False)

    def test__create_user_2(self):
        """ Test create normal User no extra data """
        user = User.objects._create_user(
            email=self.email,
            password=self.password,
            is_superuser=False
        )
        self.assertEqual(User.objects.all().count(), 1)
        self.assertEqual(user.email, self.email)
        self.assertTrue(user.check_password(self.password))
        self.assertFalse(user.is_superuser)
        self.assertEqual(user.title, '')
        self.assertEqual(user.first_name, '')
        self.assertEqual(user.last_name, '')

    def test__create_user_3(self):
        """ Test create superuser no extra data """
        user = User.objects._create_user(
            email=self.email,
            password=self.password,
            is_superuser=True
        )
        self.assertEqual(User.objects.all().count(), 1)
        self.assertEqual(user.email, self.email)
        self.assertTrue(user.check_password(self.password))
        self.assertTrue(user.is_superuser)
        self.assertEqual(user.title, '')
        self.assertEqual(user.first_name, '')
        self.assertEqual(user.last_name, '')

    def test__create_user_4(self):
        """ Test create user with extra data """
        user = User.objects._create_user(
            email=self.email,
            password=self.password,
            is_superuser=False,
            title='Dr',
            first_name='Chris',
            last_name='Bartlett'
        )
        self.assertEqual(User.objects.all().count(), 1)
        self.assertEqual(user.email, self.email)
        self.assertTrue(user.check_password(self.password))
        self.assertFalse(user.is_superuser)
        self.assertEqual(user.title, 'Dr')
        self.assertEqual(user.first_name, 'Chris')
        self.assertEqual(user.last_name, 'Bartlett')

    def test_create_user(self):
        """ Test creates normal user """
        user = User.objects.create_user(
            email=self.email,
            password=self.password
        )
        self.assertEqual(User.objects.all().count(), 1)
        self.assertEqual(user.email, self.email)
        self.assertTrue(user.check_password(self.password))
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        """ Test creates superuser """
        user = User.objects.create_superuser(
            email=self.email,
            password=self.password
        )
        self.assertEqual(User.objects.all().count(), 1)
        self.assertEqual(user.email, self.email)
        self.assertTrue(user.check_password(self.password))
        self.assertTrue(user.is_superuser)
