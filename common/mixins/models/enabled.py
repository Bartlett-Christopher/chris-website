# -*- coding: utf-8 -*-
"""
  :synopsis: mixin to add enabled boolean flag to object.

.. module:: common.mixins.models.enabled
.. author:: Chris Bartlett <chris.bartlett@therealbuzzgroup.com>
"""
from django.db import models
from django.utils.translation import ugettext_lazy as _


class EnabledMixin(models.Model):
    """Mixin to add enabled boolean field to object."""

    enabled = models.BooleanField(
        verbose_name=_('Enabled?'),
        default=True,
    )

    class Meta:
        """Metaclass for EnabledMixin."""

        abstract = True

    def enable(self, commit=True):
        """
        Enable this object.

        :param commit
        :type commit: bool
        """
        self.enabled = True

        if commit:
            self.save(update_fields=['enabled'])

    def disable(self, commit=True):
        """Disable this object."""
        self.enabled = False

        if commit:
            self.save(update_fields=['enabled'])
