# -*- coding: utf-8 -*-
"""
  :synopsis: enquiry form.

.. module: home.forms.enquiry
.. author: Chris Bartlett <bartlett.christopher.p@gmail.com>
"""
from django import forms
from django.conf import settings
from django.template import loader

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
        instance = super(EnquiryForm, self).save(commit)

        template = loader.get_template('home/email/enquiry.html')
        send_email(
            recipient=[settings.EMAIL_RECIPIENT],
            subject='Enquiry submitted.',
            text=f"Name: {self.cleaned_data['name']}\n"
                 f"Email: {self.cleaned_data['email']}\n"
                 f"Message: {self.cleaned_data['message']}\n",
            html=template.render({'instance': instance})
        )
        return instance
