# -*- coding: utf-8 -*-
"""
  :synopsis: urls for the blog app.

.. module: blog.urls
.. author: Chris Bartlett <chris.bartlett@therealbuzzgroup.com>
"""
from django.urls import path, re_path

from blog.views import BlogPostView, BlogPostListView


urlpatterns = [
    path('', BlogPostListView.as_view(), name='list'),
    re_path(r'(?P<slug>[\w-]+)/$', BlogPostView.as_view(), name='post'),
]
