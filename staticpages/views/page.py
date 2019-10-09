# -*- coding: utf-8 -*-
"""
  :synopsis: view to return a static page.

.. module: staticpages.views.page
.. author: Chris Bartlett <chris.bartlett@therealbuzzgroup.com>
"""
from django.http import HttpResponse
from django.template import loader
from django.views.generic import View

from staticpages.exceptions import PageNotFound
from staticpages.models.page import Page


class PageView(View):
    """View class for static pages."""

    def __init__(self, *args, **kwargs):
        """Initialise the page view."""
        self.page = None
        super().__init__(*args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        """
        Dispatch override to get the static page.

        Get the static page object and call through to the appropriate
        http method.

        :param request: the current request
        :type request: django.http.HttpRequest
        :return: the static page response
        :rtype: django.http.HttpResponse
        :raises: staticpages.exceptions.PageNotFound
        """
        url = kwargs.get('url', None)
        if not url:
            raise PageNotFound

        self.page = Page.get_page(url=url)

        if not self.page.enabled:
            self.page = Page.get_page(url='page-removed')

        handler = getattr(self, request.method.lower(), None)
        handler = handler or self.http_method_not_allowed

        return handler(request, *args, **kwargs)

    def get_context(self):
        """
        Build the static page template context.

        :return: the static page context
        :rtype: dict
        """
        return {
            'page': self.page
        }

    def get(self, request, *args, **kwargs):
        """
        Get request handler for a static page.

        :param request: the current request
        :type request: django.http.HttpRequest
        :return: the static page response
        :rtype: django.http.HttpResponse
        """
        template = loader.get_template(self.page.template_name)
        context = self.get_context()
        return HttpResponse(template.render(context))
