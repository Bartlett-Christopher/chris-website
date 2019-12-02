# -*- coding: utf-8 -*-
"""
  :synopsis: Unit test suite for blog post admin.

.. module: blog.tests.admin.test_blog_post
.. author: Chris Bartlett <chris.bartlett@therealbuzzgroup.com>
"""
from unittest import mock

from django.contrib.admin import AdminSite
from django.test import RequestFactory, TestCase
from django.urls import reverse
from django.utils.timezone import now
from django_dynamic_fixture import G

from authentication.models import User
from blog.admin import BlogPostAdmin
from blog.models import BlogPost


class TestBlogPostAdmin(TestCase):
    """Unit test class for BlogPostAdmin"""

    @classmethod
    def setUpClass(cls):
        super(TestBlogPostAdmin, cls).setUpClass()
        cls.site = AdminSite()
        cls.admin = BlogPostAdmin(BlogPost, cls.site)
        cls.rf = RequestFactory()

    def test_publish(self):
        unpublished = G(
            BlogPost,
            status=BlogPost.Status.DRAFT,
            published=None,
            fill_nullable_fields=False
        )
        G(
            BlogPost,
            status=BlogPost.Status.PUBLISHED,
            publoshed=now(),
            fill_nullable_fields=False
        )
        request = self.rf.get('/admin/blog-post')
        user = G(User, fill_nullable_fields=False)
        setattr(request, 'user', user)
        queryset = BlogPost.objects.all()

        with mock.patch.object(self.admin, 'message_user') as mock_msg:
            self.admin.publish(request, queryset)

        unpublished.refresh_from_db()
        self.assertEqual(unpublished.status, BlogPost.Status.PUBLISHED)
        self.assertEqual(unpublished.author, user)
        mock_msg.assert_called_once_with(
            request,
            "Successfully updated 1 blog post."
        )

    def test_get_view_on_site_url__no_obj_is_none(self):
        self.assertIsNone(
            self.admin.get_view_on_site_url(None)
        )

    def test_get_view_on_site_url__return_link(self):
        blog_post = BlogPost(slug='test-blog')

        url = self.admin.get_view_on_site_url(blog_post)

        self.assertEqual(
            url,
            reverse('blog:post', kwargs={'slug': blog_post.slug})
        )
