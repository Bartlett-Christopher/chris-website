# -*- coding: utf-8 -*-
"""
  :synopsis: BaseView for all Home app views.

.. module: home.views.base
.. author:: Chris Bartlett <bartlett.christopher.p@gmail.com>
"""
from django.views.generic import TemplateView


class BaseView(TemplateView):
    """Base view for all Home app views."""
