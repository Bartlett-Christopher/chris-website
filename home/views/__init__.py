# -*- coding: utf-8 -*-
"""
  :synopsis: views for the home app.

.. module: home.views
.. author:: Chris Bartlett <bartlett.christopher.p@gmail.com>
"""
from .contact import ContactUsView
from .landing import LandingView

__all__ = [
    'ContactUsView',
    'LandingView'
]
