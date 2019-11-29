# -*- coding: utf-8 -*-
"""
  :synopsis: urls for the blog app.

.. module: blog.urls
.. author: Chris Bartlett <chris.bartlett@therealbuzzgroup.com>
"""
from django.urls import re_path

from blog.views import BlogPostView


urlpatterns = [
    re_path(r'(?P<slug>[\w-]+)/$', BlogPostView.as_view(), name='post')
]
