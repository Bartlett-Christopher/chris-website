# -*- codingL utf-8 -*-
"""
.. module: home.about
  :synopsis: view for about page
.. module author: Chris Bartlett <bartlett.christopher.p@gmail.com>
"""
from django.views.generic import TemplateView


class AboutView(TemplateView):
    """ View for about page """
    template_name = 'home/about.html'
