# -*- coding: utf-8 -*-
"""
.. module:: staticpages.admin.staticpage
   :synopsis: Admin class for StaticPage model

.. moduleauthor:: Chris Bartlett <chris.bartlett@therealbuzzgroup.com>
"""
from django.contrib import admin

from staticpages.models.staticpage import StaticPage


@admin.register(StaticPage)
class StaticPageAdmin(admin.ModelAdmin):
    """
    Admin class for StaticPage
    """
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
        'modified'
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
