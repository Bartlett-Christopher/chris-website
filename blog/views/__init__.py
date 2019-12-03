# -*- coding: utf-8 -*-
"""
  :synopsis: Views for the blog app.

.. module: blog.views
.. author: Chris Bartlett <chris.bartlett@therealbuzzgroup.com>
"""
from blog.views.blog_post import BlogPostView
from blog.views.blog_list import BlogPostListView

__all__ = [
    'BlogPostView',
    'BlogPostListView',
]
