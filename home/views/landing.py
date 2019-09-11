# -*- coding: utf-8 -*-
"""
.. module: home.views.landing
  :synopsis: Home page LandingView

.. moduleauthor:: Chris Bartlett <bartlett.christopher.p@gmail.com>
"""
from .base import BaseView


class LandingView(BaseView):
    """
    View for main landing page
    """
    template_name = 'home/landing.html'

    pass
