# -*- coding: utf-8 -*-
"""
  :synopsis: View for listing blog posts.

.. module: blog.views.blog_list
.. author: Chris Bartlett <chris.bartlett@therealbuzzgroup.com>
"""
from django.views.generic import TemplateView

from blog.models import BlogPost


class BlogPostListView(TemplateView):
    """View for listing blog posts."""

    template_name = 'blog/blog_list.html'

    def get(self, request, *args, **kwargs):
        """
        Display list of blog posts.

        :param request: the current request
        :type request: django.http.HttpRequest
        :return: the blog page list response
        :rtype: django.http.HttpResponse
        """
        blogs = BlogPost.objects.filter(
            status=BlogPost.Status.PUBLISHED,
            published__isnull=False
        ).order_by('-published')

        return self.render_to_response(
            context={
                'blogs': blogs
            }
        )
