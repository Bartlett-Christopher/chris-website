# -*- coding: utf-8 -*-
"""
  :synopsis: Admin mixin to generate a 'view on site' link in admin list view.

.. module: common.mixins.admin.view_on_site
.. author: Chris Bartlett <chris.bartlett@therealbuzzgroup.com>
"""
from django.contrib import admin
from django.utils.safestring import mark_safe


class ViewOnSiteMixin(admin.ModelAdmin):
    """Admin mixin class to add 'view on site' url."""

    def __init__(self, *args, **kwargs):
        """Override init to inject 'view on site' list display link."""
        super(ViewOnSiteMixin, self).__init__(*args, **kwargs)
        self.list_display = self.list_display + ('view_on_site',)

    def view_on_site(self, obj):
        """
        Construct link for the admin list view to view object on the site.

        :param obj: the object to view
        :type obj: django.db.models.Model
        :return: link to view the object
        :rtype: django.utils.safestring.SafeText
        """
        link = f"<a href='{self.get_view_on_site_url(obj)}' target='_blank'>" \
               f"View on site</a>"

        return mark_safe(link)
