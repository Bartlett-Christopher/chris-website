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

    actions = ['resolve_enquiries']

    def resolve_enquiries(self, request, queryset):
        """
        Enquiry admin action to resolve multiple enquiries.

        :param request: the current request
        :type request: django.http.HttpResponse
        :param queryset: the enquiry queryset
        :type queryset: django.db.models.query.QuerySet
        """
        queryset.update(resolved=True)
        resolved = queryset.count()
        message = f"Successfully resolved {resolved} " \
                  f"{'enquiry' if resolved == 1 else 'enquiries'}."
        self.message_user(request, message)
