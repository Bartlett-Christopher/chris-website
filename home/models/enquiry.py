# -*- coding: utf-8 -*-
"""
  :synopsis: user enquiry model.

.. module: home.models.enquiry
.. author: Chris Bartlett <chris.bartlett@therealbuzzgroup.com>
"""
from django.db import models
from django.utils.translation import ugettext_lazy as _

from common.mixins.models import TimeStampMixin


class Enquiry(TimeStampMixin):
    """Model to describe a user enquiry."""

    name = models.CharField(
        verbose_name=_('Name'),
        max_length=255,
        blank=False,
        null=False,
        help_text=_('The name supplied by the enquiring user.')
    )

    email = models.EmailField(
        verbose_name=_('Email address'),
        blank=False,
        null=False,
        help_text=_('The email address supplied by the enquiring user.')
    )

    message = models.TextField(
        verbose_name=_('Message'),
        blank=False,
        null=False,
        help_text=_('The user enquiry.')
    )

    resolved = models.BooleanField(
        verbose_name=_('Enquiry resolved?'),
        default=False,
        null=False,
        help_text=_('Indicates if this enquiry has been resolved.')
    )
