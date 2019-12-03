"""
  :synopsis: Django app config for blog app.

.. :module: blog.apps
.. :author: Chris Bartlett <bartlett.christopher.p@gmail.com>
"""
from django.apps import AppConfig


class BlogConfig(AppConfig):
    """Blog app config."""

    name = 'blog'
