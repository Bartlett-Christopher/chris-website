# -*- coding: utf-8 -*-
"""
  :synopsis: unit test suite for blog post view.

.. module: blog.test.views.test_blog_post
.. author: Chris Bartlett <chris.bartlett@therealbuzzgroup.com>
"""
from django.http import Http404
from django.test import RequestFactory, TestCase
from django_dynamic_fixture import G

from blog.models import BlogPost
from blog.views import BlogPostView


class TestBlogPostView(TestCase):
    """Unit test class for blog post view."""

    @classmethod
    def setUpClass(cls):
        super(TestBlogPostView, cls).setUpClass()
        cls.rf = RequestFactory()
        cls.slug = 'my-test-slug'
        cls.request = cls.rf.get('/blog/' + cls.slug)
        cls.post = G(BlogPost, slug=cls.slug)
        cls.view = BlogPostView()
        setattr(cls.view, 'request', cls.request)

    @classmethod
    def tearDownClass(cls):
        BlogPost.objects.all().delete()
        super(TestBlogPostView, cls).tearDownClass()

    def test_get__no_slug_kwarg_raises_404(self):
        with self.assertRaises(Http404):
            self.view.get(self.request)

    def test_get__post_does_not_exist_raises_404(self):
        with self.assertRaises(Http404):
            self.view.get(self.request, slug='unknown')

    def test_get__post_exists_returns_page(self):
        response = self.view.get(self.request, slug=self.slug)

        self.assertEqual(response.context_data['blog_post'], self.post)
