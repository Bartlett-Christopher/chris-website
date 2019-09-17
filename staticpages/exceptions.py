# -*- coding: utf-8 -*-
"""
.. module:: .exceptions
   :synopsis: exception for the staticpages app

.. moduleauthor:: Chris Bartlett <chris.bartlett@therealbuzzgroup.com>
"""


class BaseStaticPageException(Exception):
    """ Base exception for all StaticPage exceptions """
    pass


class StaticPageNotFound(BaseStaticPageException):
    """ StaticPage Exception raised when no StaticPage found """
    pass
