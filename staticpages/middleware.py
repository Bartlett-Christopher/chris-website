# -*- coding: utf-8 -*-
"""
.. module:: staticpages.middleware
   :synopsis: middleware to capture a 404 response and return a static page

.. moduleauthor:: Chris Bartlett <chris.bartlett@therealbuzzgroup.com>
"""
from common.mixins.middleware import MiddlewareMixin
from staticpages.exceptions import BasePageException
from staticpages.views.page import PageView


class StaticPageCaptureMiddleware(MiddlewareMixin, object):
    """
    Middleware to intercept a 404 response thrown by Django url resolving and
    return a static page if one found with appropriate url.
    Otherwise, fall through and continue to raise 404.
    """

    def process_response(self, request, response):
        """
        If the response is a 404, check for a static page and return it,
        otherwise fall through

        :param request: the current request
        :type request: django.http.HttpRequest
        :param response: the 404 response
        :type response: django.http.HttpResponse
        :return: the static page response
        :rtype: django.http.HttpResponse
        """
        if response.status_code != 404:
            return response

        view = PageView()

        try:
            response = view.dispatch(request, url=request.path_info)
        except BasePageException:
            return response

        return response
