# -*- coding: utf-8 -*-
"""
:synopsis: custom User model for the authentication app.

.. module: authentication.models.user
.. author: Chris Bartlett <bartlett.christopher.p@gmail.com>
"""
from django.contrib.auth.models import BaseUserManager
from django.utils import timezone


class UserManager(BaseUserManager):
    """Custom UserManager for User model."""

    def get_by_email(self, email):
        """
        Get User object by email.

        :param email: user email
        :type email: str
        :return: the User instance
        :rtype: authentication.models.user.User
        :raises: DoesNotExist
        """
        return self.get(email=email.lower())

    def _create_user(self, email, password, is_superuser,
                     **extra_fields):
        """
        Create a User with the specified attributes.

        :param email: User email
        :type email: six.text_type
        :param password: User password
        :type password: six.text_type
        :param is_superuser: designates whether User is superuser
        :type is_superuser: bool
        :param extra_fields: extra fields to set into the User
        :type extra_fields: dict
        :return: the created User
        :rtype: authentication.User
        """
        if not email:
            raise ValueError('Email must be set')

        email = self.normalize_email(email)
        user = self.model(
            email=email,
            is_superuser=is_superuser,
            last_login=timezone.now(),
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, email, password, **extra_fields):
        """
        Create a normal User with the specified email and password.

        :param email: User email
        :type email: six.text_type
        :param password: User password
        :type password: six.text_type
        :param extra_fields: extra fields to set into the User
        :type extra_fields: dict
        :return: the created User
        :rtype: authentication.User
        """
        return self._create_user(email, password, False, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """
        Create a super User with the specified email and password.

        :param email: User email
        :type email: six.text_type
        :param password: User password
        :type password: six.text_type
        :param extra_fields: extra fields to set into the User
        :type extra_fields: dict
        :return: the created super User
        :rtype: authentication.User
        """
        return self._create_user(email, password, True, **extra_fields)
