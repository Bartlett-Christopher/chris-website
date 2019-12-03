# -*- coding: utf-8 -*-
"""
  :synopsis: View for a blog post.

.. module: blog.views.blog_post
.. author: Chris Bartlett <chris.bartlett@therealbuzzgroup.com>
"""
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from blog.models import BlogPost


class BlogPostView(TemplateView):
    """View for a blog post."""

    template_name = 'blog/blog_post.html'

    def get(self, request, *args, **kwargs):
        """
        Return a blog post page or 404.

        :param request: the current request
        :type request: django.http.HttpRequest
        :return: the blog page response or 404
        :rtype: django.http.HttpResponse
        """
        slug = kwargs.get('slug')

        if slug is None:
            raise Http404

        blog_post = get_object_or_404(BlogPost, slug=slug)

        return self.render_to_response(
            context={
                'blog_post': blog_post
            }
        )
