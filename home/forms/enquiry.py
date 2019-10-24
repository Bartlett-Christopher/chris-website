# -*- coding: utf-8 -*-
"""
  :synopsis: enquiry form.

.. module: home.forms.enquiry
.. author: Chris Bartlett <bartlett.christopher.p@gmail.com>
"""
from django import forms
from django.conf import settings

from common.utils.email import send_email
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
        """
        Save the enquiry and send notification email.

        :param commit: whether the commit the data to the database
        :type commit: bool
        :return: the enquiry instance
        :rtype: home.models.enquiry.Enquiry
        """
        send_email(
            to=[settings.EMAIL_RECIPIENT],
            subject='Enquiry submitted.',
            text=self.cleaned_data['message']
        )
        instance = super(EnquiryForm, self).save(commit)
        return instance
