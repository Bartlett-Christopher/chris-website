# -*- coding: utf-8 -*-
"""
  :synopsis: Admin page for blog posts.

.. module: blog.admin.blog_post
.. author: Chris Bartlett <chris.bartlett@therealbuzzgroup.com>
"""
from django.contrib import admin
from django.utils.timezone import now

from blog.models.blog_post import BlogPost


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    """Admin class for BlogPost model."""

    fieldsets = (
        (None, {
            'fields': (
                'title',
                'slug',
                'author',
                'content',
            )
        }),
        ('Status', {
            'fields': (
                'status',
                'enabled'
            )
        }),
        ('Dates', {
            'fields': (
                'created',
                'modified',
                'published'
            )
        })
    )

    list_display = (
        'title',
        'slug',
        'enabled',
        'status',
        'author',
    )

    list_filter = (
        'status',
        'author',
    )

    list_editable = (
        'enabled',
    )

    readonly_fields = (
        'created',
        'modified',
        'published',
    )

    search_fields = (
        'title',
    )

    actions = (
        'publish',
    )

    def publish(self, request, queryset):
        """
        Admin action to publish selected blog posts.

        :param request: current request
        :type request: django.http.HttpRequest
        :param queryset: selected blog posts
        :type queryset: django.db.models.query.QuerySet
        """
        updated = queryset.exclude(
            status=BlogPost.Status.PUBLISHED
        ).update(
            author=request.user,
            published=now(),
            status=BlogPost.Status.PUBLISHED
        )

        self.message_user(
            request,
            f"Successfully updated {updated} "
            f"blog post{'' if updated == 1 else 's'}."
        )
