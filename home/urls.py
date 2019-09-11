# -*- coding: utf-8 -*-
"""
.. module: home.urls
  :synopsis: urls for the home app
.. module author: Chris Bartlett <bartlett.christopher.p@gmail.com>
"""
from django.urls import path

from home.views.about import AboutView
from home.views.landing import LandingView


urlpatterns = [
    path('', LandingView.as_view(), name='landing'),
    path('about/', AboutView.as_view(), name='about'),
]
