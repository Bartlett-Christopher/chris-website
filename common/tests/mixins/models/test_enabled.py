# -*- coding: utf-8 -*-
"""
.. module:: commons.tests.mixins.models.test_enabled
   :synopsis: unit tests for EnabledMixin

.. moduleauthor:: Chris Bartlett <chris.bartlett@therealbuzzgroup.com>
"""
from unittest.mock import patch

from django.test import TestCase

from common.mixins.models.enabled import EnabledMixin


class TestEnabledMixin(TestCase):
    """ Unit test class for EnabledMixin """

    def test_construction__default(self):
        mixin = EnabledMixin()

        self.assertTrue(mixin.enabled)

    def test_enable__no_commit(self):
        mixin = EnabledMixin(enabled=False)

        with patch.object(mixin, 'save') as mock_save:
            mixin.enable(commit=False)

        self.assertTrue(mixin.enabled)
        mock_save.assert_not_called()

    def test_enable__with_commit(self):
        mixin = EnabledMixin(enabled=False)

        with patch.object(mixin, 'save') as mock_save:
            mixin.enable(commit=True)

        self.assertTrue(mixin.enabled)
        mock_save.assert_called_once_with(
            update_fields=['enabled']
        )

    def test_disable__no_commit(self):
        mixin = EnabledMixin(enabled=True)

        with patch.object(mixin, 'save') as mock_save:
            mixin.disable(commit=False)

        self.assertFalse(mixin.enabled)
        mock_save.assert_not_called()

    def test_disable__with_commit(self):
        mixin = EnabledMixin(enabled=True)

        with patch.object(mixin, 'save') as mock_save:
            mixin.disable(commit=True)

        self.assertFalse(mixin.enabled)
        mock_save.assert_called_once_with(
            update_fields=['enabled']
        )
