# -*- coding: utf-8 -*-
"""
.. module:: staticpages.admin.page
   :synopsis: Admin class for Page model

.. moduleauthor:: Chris Bartlett <chris.bartlett@therealbuzzgroup.com>
"""
from django.contrib import admin
from django.utils.safestring import mark_safe

from staticpages.models.page import Page


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    """
    Admin class for Page model
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
        'modified',
        'view_on_site'
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

    def view_on_site(self, obj):
        """
        Construct link for the admin list view to view static page on the site

        :param obj: the static page object
        :type obj: staticpages.models.Page
        :return: link to view the static page
        :rtype: django.utils.safestring.SafeText
        """
        link = '''<a href="{url}" target="_blank">{text}</a>'''.format(
            url=self.get_view_on_site_url(obj),
            text='View on site'
        )
        return mark_safe(link)

    def get_view_on_site_url(self, obj=None):
        """
        Override of BaseModelAdmin to return static page url if available

        :param obj: static page or None
        :type obj: staticpages.models.page.Page or NoneType
        """
        return obj.url if obj else None
