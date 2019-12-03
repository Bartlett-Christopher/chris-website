# -*- coding: utf-8 -*-
"""
  :synopsis: unit test suite for blog post model.

.. module: .test_blog_post
.. author: Chris Bartlett <chris.bartlett@therealbuzzgroup.com>
"""
from django.test import TestCase
from django.utils.text import slugify
from django.utils.timezone import now
from django_dynamic_fixture import G

from authentication.models import User
from blog.models import BlogPost


class TestBlogPost(TestCase):
    """Unit test class for blog post model."""

    def test_is_published__draft_status(self):
        post = BlogPost(status=BlogPost.Status.DRAFT, published=None)
        self.assertFalse(post.is_published)

    def test_is_published__published_status_no_timestamp(self):
        post = BlogPost(status=BlogPost.Status.PUBLISHED, published=None)
        self.assertFalse(post.is_published)

    def test_is_published__published_timestamp_draft_status(self):
        post = BlogPost(status=BlogPost.Status.DRAFT, published=now())
        self.assertFalse(post.is_published)

    def test_is_published__published_status_and_timestamp(self):
        post = BlogPost(status=BlogPost.Status.PUBLISHED, published=now())
        self.assertTrue(post.is_published)

    def test_publish__commit_false(self):
        user = User()
        post = BlogPost(
            status=BlogPost.Status.DRAFT,
            published=None,
            author=None
        )

        post.publish(user, commit=False)

        self.assertEqual(post.author, user)
        self.assertIsNotNone(post.published)
        self.assertEqual(post.status, BlogPost.Status.PUBLISHED)

    def test_publish__commit_true(self):
        user = G(User, fill_nullable_fields=False)
        post = G(
            BlogPost,
            status=BlogPost.Status.DRAFT,
            published=None,
            author=None,
            fill_nullable_fields=False
        )

        post.publish(user)

        saved_post = BlogPost.objects.get(id=post.id)
        self.assertEqual(saved_post.author, user)
        self.assertIsNotNone(saved_post.published)
        self.assertEqual(saved_post.status, BlogPost.Status.PUBLISHED)

    def test_set_blog_post_slug__slug_is_none(self):
        post = BlogPost(title='My test blog', slug=None)

        post.save()

        self.assertEqual(post.slug, slugify('My test blog'))

    def test_set_blog_post_slug__slug_is_not_none(self):
        post = BlogPost(title='My test blog', slug='my-custom-slug')

        post.save()

        self.assertEqual(post.slug, 'my-custom-slug')
