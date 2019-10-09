# -*- coding: utf-8 -*-
"""
  :synopsis: exceptions for the staticpages app.

.. module: staticpages.exceptions
.. author: Chris Bartlett <chris.bartlett@therealbuzzgroup.com>
"""


class BasePageException(Exception):
    """Base exception for all Page exceptions."""


class PageNotFound(BasePageException):
    """Exception raised when no Page found."""
