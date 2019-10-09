# -*- coding: utf-8 -*-
"""
  :synopsis: urls for the home app.

.. module: home.urls
.. author: Chris Bartlett <bartlett.christopher.p@gmail.com>
"""
from django.urls import path

from home.views.landing import LandingView


urlpatterns = [
    path('', LandingView.as_view(), name='landing'),
]
