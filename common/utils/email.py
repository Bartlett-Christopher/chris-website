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
def send_email(to, subject, text,
               html=None, sender=settings.DEFAULT_FROM_EMAIL):
    """
    Utility function to send an email.

    """
    if not isinstance(to, (list, tuple)):
        to = [to]

    if settings.EMAIL_DEBUG:
        recipients = ','.join(to)
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
            recipient_list=to,
            fail_silently=False,
            html_message=html
        )
