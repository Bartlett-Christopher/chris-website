# -*- coding: utf-8 -*-
"""
.. module: home.views.landing
  :synopsis: view for main landing page
.. module author: Chris Bartlett <bartlett.christopher.p@gmail.com>
"""
from django.views.generic import TemplateView


class LandingView(TemplateView):
    """
    View for main landing page
    """
    template_name = 'home/landing.html'
