# -*- coding: utf-8 -*-
"""
  :synopsis: contact us form.

.. module: home.forms.contact
.. author: Chris Bartlett <bartlett.christopher.p@gmail.com>
"""
from django.forms import forms


class ContactUsForm(forms.Form):
    """Contact us form."""

    def send_mail(self):
        """
        Send emails.

        - to user with confirmation of request
        - to self with details of contact
        """
