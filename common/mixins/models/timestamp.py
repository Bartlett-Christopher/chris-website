# -*- coding: utf-8 -*-
"""
  :synopsis: mixin to add time stamping fields to object.

.. module:: common.mixins.models.timestamp
.. author:: Chris Bartlett <chris.bartlett@therealbuzzgroup.com>
"""
from django.db import models
from django.utils.translation import ugettext_lazy as _


class TimeStampMixin(models.Model):
    """Mixin to add created and modified timestamps."""

    created = models.DateTimeField(
        verbose_name=_('Date object created'),
        editable=False,
        auto_now_add=True,
        help_text=_('Date and time that this object was created.')
    )
    modified = models.DateTimeField(
        verbose_name=_('Date object last modified'),
        editable=False,
        auto_now=True
    )

    class Meta:
        """Metadata for TimeStampMixin."""

        abstract = True
