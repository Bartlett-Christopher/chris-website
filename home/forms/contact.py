# -*- coding: utf-8 -*-
"""
  :synopsis: contact us form.

.. module: home.forms.contact
.. author: Chris Bartlett <bartlett.christopher.p@gmail.com>
"""
from django import forms


class ContactUsForm(forms.Form):
    """Contact us form."""

    recipient_list = ['christopherbartlett@hotmail.co.uk']

    name = forms.CharField(
        max_length=255,
        required=True,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Your name'
            }
        )
    )
    email_address = forms.EmailField(
        max_length=255,
        required=True,
        widget=forms.EmailInput(
            attrs={
                'placeholder': 'Your email'
            }
        )
    )

    message = forms.CharField(
        required=True,
        widget=forms.Textarea(
            attrs={
                'placeholder': 'Your message'
            }
        ),
    )

    def send_email(self):
        print('Sending email')
