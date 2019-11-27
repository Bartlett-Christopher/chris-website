# -*- coding: utf-8 -*-
"""
  :synopsis: utility module containing functionality for emailing.

.. module: common.utils.email
.. author: Chris Bartlett <chris.bartlett@therealbuzzgroup.com>
"""
from background_task import background

from django.conf import settings
from django.core.mail import send_mail as django_send_mail


@background(schedule=settings.EMAIL_DELAY, queue='email')
def send_email(recipient, subject, text,
               html=None, sender=settings.DEFAULT_FROM_EMAIL):
    """
    Send an email.

    :param recipient: recipient(s) email address
    :type recipient: str or list[str]
    :param subject: email subject line
    :type subject: str
    :param text: email content
    :type text: str
    :param html: email HTML content or None
    :type html: str
    :param sender: sender email address
    :type sender: str
    """
    if not isinstance(recipient, (list, tuple)):
        recipient = [recipient]

    if settings.EMAIL_DEBUG:
        recipients = ','.join(recipient)
        print(
            f'sending email...\n'
            f'from: {sender}\n'
            f'to: {recipients}\n'
            f'subject: {subject}'
        )
    else:
        django_send_mail(
            subject=subject,
            message=text,
            from_email=sender,
            recipient_list=recipient,
            fail_silently=False,
            html_message=html
        )
