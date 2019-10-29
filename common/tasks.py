# -*- coding: utf-8 -*-
"""
:synopsis: background tasks for common app.

.. module: common.tasks
.. author: Chris Bartlett <chris.bartlett@therealbuzzgroup.com>
"""
from common.utils.email import send_email

__all__ = [
    'send_email'
]
