# -*- coding: utf-8 -*-
"""
.. module:: common.mixins.middleware
   :synopsis: mixin to provide common middleware methods

.. moduleauthor:: Chris Bartlett <chris.bartlett@therealbuzzgroup.com>
"""


class MiddlewareMixin(object):
    """ Mixin to provide common Django middleware methods """

    def __init__(self, get_response):
        """
        Store the get_response method onto the object

        :param get_response: method to get response from request
        :type get_response: callable
        """
        self.get_response = get_response
        super().__init__()

    def __call__(self, request):
        """
        Process the incoming request and return a response

        :param request: the incoming request
        :type request: django.http.HttpRequest
        :return: the resultant response
        :rtype: django.http.HttpResponse
        """
        response = None
        if hasattr(self, 'process_request'):
            response = self.process_request(request)

        response = response or self.get_response(request)

        if hasattr(self, 'process_response'):
            response = self.process_response(request, response)

        return response
