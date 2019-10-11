# -*- coding: utf-8 -*-
"""
  :synopsis: admin module for enquiry model.

.. module: home.admin.enquiry
.. author: Chris Bartlett <chris.bartlett@therealbuzzgroup.com>
"""
from django.contrib import admin

from home.models import Enquiry


@admin.register(Enquiry)
class EnquiryAdmin(admin.ModelAdmin):
    """Admin class for Enquiry model."""

    fieldsets = (
        (None, {
            'fields': (
                'name',
                'email',
                'message',
                'notes',
            )
        }),
        ('Info', {
            'fields': (
                'resolved',
                'created',
                'modified'
            )
        })
    )

    list_display = (
        'name',
        'email',
        'resolved',
        'created'
    )

    list_filter = (
        'resolved',
        'created'
    )

    readonly_fields = (
        'name',
        'email',
        'message',
        'created',
        'modified'
    )

    search_fields = (
        'name',
        'email'
    )
