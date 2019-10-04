# -*- coding: utf-8 -*-
"""
:synopsis: custom User model for the authentication app.

.. module: authentication.models.user
.. author: Chris Bartlett <bartlett.christopher.p@gmail.com>
"""
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy as _

from authentication.manager import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom User class.

    - Replaces django.contrib.auth.models.user
    - Provides all custom fields required for this site
    """

    USERNAME_FIELD = 'email'

    email = models.EmailField(
        verbose_name=_('Email address'),
        max_length=255,
        unique=True,
        db_index=True
    )
    title = models.CharField(
        verbose_name=_('Title'),
        max_length=30,
        blank=True,
        default='',
        db_index=True,
        null=True
    )
    first_name = models.CharField(
        verbose_name=_('First name'),
        max_length=100,
        blank=True,
        db_index=True
    )
    last_name = models.CharField(
        verbose_name=_('Last name'),
        max_length=100,
        blank=True,
        db_index=True
    )

    objects = UserManager()

    class Meta:
        """Metadata for the User model."""

        app_label = 'authentication'
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def __str__(self):
        """Display object as string."""
        return '{name} ({email})'.format(
            name=self.name,
            email=self.email
        )

    @property
    def name(self):
        """
        User name property.

        :return: human readable name
        :rtype: six.text_type
        """
        parts = [
            self.title,
            self.first_name,
            self.last_name,
        ]
        return ' '.join([
            force_text(part)
            for part in parts
            if part
        ])

    @property
    def is_staff(self):
        """
        User property - is_staff and is_superuser are equivalent.

        :return: whether User is staff member
        :rtype: bool
        """
        return self.is_superuser
