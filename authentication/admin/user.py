# -*- coding: utf-8 -*-
"""
:synopsis: custom User admin for the authentication app.

.. module: authentication.admin.user
.. author: Chris Bartlett <bartlett.christopher.p@gmail.com>
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as UserAdmin_
from django.utils.translation import ugettext_lazy as _

from authentication.models import User


@admin.register(User)
class UserAdmin(UserAdmin_, admin.ModelAdmin):
    """Custom Admin class for the User model."""

    list_display = (
        'id',
        'email',
        'first_name',
        'last_name',
    )

    list_filter = ()

    ordering = (
        'id',
    )

    search_fields = (
        'id',
        'email',
        'first_name',
        'last_name',
    )

    fieldsets = (
        (_('Personal info'), {
            'fields': (
                'email',
                'title',
                'first_name',
                'last_name',
            ),
        }),
        (_('Permissions'), {
            'fields': (
                'is_superuser',
                'groups',
                'user_permissions',
            )
        }),
    )

    add_fieldsets = (
        (None, {
            'fields': (
                'email',
                'title',
                'first_name',
                'last_name',
                'password1',
                'password2',
            )
        }),
    )
