# -*- coding: utf-8 -*-
"""
.. module: home.views.landing
  :synopsis: Home page LandingView

.. moduleauthor:: Chris Bartlett <bartlett.christopher.p@gmail.com>
"""
from .base import BaseView


class LandingView(BaseView):
    """ Home page landing view """
    template_name = 'landing.html'

    pass
