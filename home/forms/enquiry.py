# -*- coding: utf-8 -*-
"""
  :synopsis: enquiry form.

.. module: home.forms.enquiry
.. author: Chris Bartlett <bartlett.christopher.p@gmail.com>
"""
from django import forms

from home.models import Enquiry


class EnquiryForm(forms.ModelForm):
    """Enquiry form."""

    class Meta:
        """Metadata for Enquiry model form."""
        model = Enquiry
        fields = (
            'name',
            'email',
            'message'
        )

    recipient_list = ['christopherbartlett@hotmail.co.uk']

    def save(self, commit=True):
        print('email notification sent')
        instance = super(EnquiryForm, self).save(commit)
        return instance
