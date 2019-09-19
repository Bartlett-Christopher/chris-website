# -*- coding: utf-8 -*-
"""
.. module:: staticpages.exceptions
   :synopsis: exception for the staticpages app

.. moduleauthor:: Chris Bartlett <chris.bartlett@therealbuzzgroup.com>
"""


class BasePageException(Exception):
    """ Base exception for all Page exceptions """
    pass


class PageNotFound(BasePageException):
    """ Exception raised when no Page found """
    pass
