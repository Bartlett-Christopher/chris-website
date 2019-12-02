# -*- coding: utf-8 -*-
"""
  :synopsis: unit test suite for blog list view.

.. module: blog.tests.test_blog_list
.. author: Chris Bartlett <chris.bartlett@therealbuzzgroup.com>
"""
from unittest import mock

from django.test import RequestFactory, TestCase
from django.utils.timezone import now
from django_dynamic_fixture import G

from blog.models import BlogPost
from blog.views import BlogPostListView


class TestBlogPostListView(TestCase):
    """Unit test class for BlogPostListView."""

    def test_get(self):
        BlogPost.objects.count()
        G(
            BlogPost,
            status=BlogPost.Status.DRAFT,
            published=None,
            fill_nullable_fields=False
        )
        G(
            BlogPost,
            status=BlogPost.Status.DRAFT,
            published=now(),
            fill_nullable_fields=False
        )
        G(
            BlogPost,
            status=BlogPost.Status.PUBLISHED,
            published=None,
            fill_nullable_fields=False
        )
        post = G(
            BlogPost,
            status=BlogPost.Status.PUBLISHED,
            published=now(),
            fill_nullable_fields=False
        )

        rf = RequestFactory()
        request = rf.get('/blogs/')

        view = BlogPostListView()
        setattr(view, 'request', request)
        result = view.get(request)

        self.assertEqual(BlogPost.objects.count(), 4)
        self.assertListEqual(list(result.context_data['blogs']), [post])
