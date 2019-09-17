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
    pass
