# -*- coding: utf-8 -*-
"""
.. module:: staticpages.views.staticpage
   :synopsis: view to return a static page

.. moduleauthor:: Chris Bartlett <chris.bartlett@therealbuzzgroup.com>
"""
from django.http import HttpResponse
from django.template import loader, RequestContext
from django.views.generic import View

from staticpages.exceptions import StaticPageNotFound
from staticpages.models.staticpage import StaticPage


class StaticPageView(View):
    """ View class for static pages """

    def __init__(self, *args, **kwargs):
        self.page = None
        super().__init__(*args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        """
        Dispatch override to get the static page object and call through to
        the appropriate http method

        :param request: the current request
        :type request: django.http.HttpRequest
        :return: the static page response
        :rtype: django.http.HttpResponse
        """
        url = kwargs.get('url', None)
        if not url:
            raise StaticPageNotFound

        self.page = StaticPage.get_page(url=url)

        handler = getattr(self, request.method.lower(), None)
        handler = handler or self.http_method_not_allowed

        return handler(request, *args, **kwargs)

    def get_context(self):
        """
        Build the static page template context

        :return: the static page context
        :rtype: dict
        """
        return {
            'page': self.page
        }

    def get(self, request, *args, **kwargs):
        """
        Handler for getting a static page

        :param request: the current request
        :type request: django.http.HttpRequest
        :return: the static page response
        :rtype: django.http.HttpResponse
        """
        template = loader.get_template(self.page.template_name)
        context = self.get_context()
        return HttpResponse(template.render(context))
