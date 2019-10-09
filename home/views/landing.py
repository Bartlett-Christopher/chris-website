# -*- coding: utf-8 -*-
"""
  :synopsis: home page LandingView.

.. module: home.views.landing
.. author: Chris Bartlett <bartlett.christopher.p@gmail.com>
"""
from .base import BaseView


class LandingView(BaseView):
    """View for main landing page."""

    template_name = 'home/landing.html'
