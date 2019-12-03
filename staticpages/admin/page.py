# -*- coding: utf-8 -*-
"""
  :synopsis: Admin class for Page model.

.. module: staticpages.admin.page
.. author: Chris Bartlett <chris.bartlett@therealbuzzgroup.com>
"""
from django.contrib import admin

from common.mixins.admin import ViewOnSiteMixin
from staticpages.models.page import Page


@admin.register(Page)
class PageAdmin(ViewOnSiteMixin, admin.ModelAdmin):
    """Admin class for Page model."""

    fieldsets = (
        (None, {
            'fields': (
                'enabled',
                'url',
                'title',
                'template_name',
                'content'
            )
        }),
        ('Dates', {
            'fields': (
                'created',
                'modified'
            )
        })
    )
    list_display = (
        'title',
        'url',
        'template_name',
        'enabled',
        'modified',
    )

    list_filter = (
        'enabled',
    )
    list_editable = (
        'enabled',
    )
    readonly_fields = (
        'created',
        'modified'
    )
    search_fields = (
        'url',
        'title',
        'content'
    )

    def get_view_on_site_url(self, obj=None):
        """
        Override of BaseModelAdmin to return static page url if available.

        :param obj: static page or None
        :type obj: staticpages.models.page.Page or NoneType
        """
        return obj.url if obj else None
