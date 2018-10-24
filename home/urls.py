# -*- coding: utf-8 -*-
"""
.. module: home.urls
  :synopsis: Urls for the Home app

.. moduleauthor:: Chris Bartlett <bartlett.christopher.p@gmail.com>
"""
from django.urls import path

from .views import LandingView

urlpatterns = [
    path('', LandingView.as_view(), name='landing')
]
