# -*- coding: utf-8 -*-
"""
  :synopsis: Model to describe a blog post.

.. module: blog.models.blog
.. author: Chris Bartlett <chris.bartlett@therealbuzzgroup.com>
"""
from ckeditor import fields

from django.conf import settings
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _

from common.mixins.models.enabled import EnabledMixin
from common.mixins.models.timestamp import TimeStampMixin


class BlogPost(EnabledMixin, TimeStampMixin, models.Model):
    """Model to describe a blog post."""

    class Status:
        """Blog statuses."""

        DRAFT = 0
        PUBLISHED = 1

        CHOICES = (
            (DRAFT, _('Draft')),
            (PUBLISHED, _('Published')),
        )

    title = models.CharField(
        verbose_name=_('Title'),
        max_length=255,
        help_text=_('Title of the blog post.')
    )

    content = fields.RichTextField(
        verbose_name=_('Content'),
        blank=True,
        null=True,
        help_text=_('Content of the blog post.')
    )

    slug = models.SlugField(
        verbose_name=_('Slug'),
        unique=True,
        max_length=255,
        default=None,
        null=True,
        blank=True,
        help_text=_('URL slug of the blog post.')
    )

    author = models.ForeignKey(
        verbose_name=_('Author'),
        to=settings.AUTH_USER_MODEL,
        on_delete=models.deletion.SET_NULL,
        related_name='blogs',
        null=True,
        blank=True,
        help_text=_('The author of this blog post.')
    )

    status = models.IntegerField(
        verbose_name=_('Status'),
        choices=Status.CHOICES,
        default=Status.DRAFT,
        help_text=_('The status of the blog post.')
    )

    published = models.DateTimeField(
        verbose_name=_('Published'),
        null=True,
        blank=True,
        help_text=_('Date blog post published.')
    )

    class Meta:
        """Metaclass for Blog model."""

        app_label = 'blog'
        verbose_name = _('Blog post')
        verbose_name_plural = _('Blog posts')

    @property
    def is_published(self):
        """
        Is this blog post published?

        :return: whether this blog post is published
        :rtype: bool
        """
        return self.status == self.Status.PUBLISHED and \
            self.published is not None

    def publish(self, user, commit=True):
        """
        Publish this blog post.

        Performs the following actions:
        - sets status to published
        - sets published date to now
        - sets author to one supplied

        :param user: user publishing this blog post
        :type user: authentication.models.user.User
        :param commit: whether to save to database
        :type commit: bool
        """
        self.author = user
        self.published = now()
        self.status = self.Status.PUBLISHED

        if commit:
            self.save(update_fields=['author', 'published', 'status'])


@receiver(pre_save, sender=BlogPost)
def set_blog_post_slug(sender, instance, **kwargs):  # pylint: disable=W0613
    """
    Set the blog post slug as the slugified title if custom slug not specified.

    :param sender: sender class
    :type sender: blog.models.blog_post.BlogPost
    :param instance: model instance
    :type instance: blog.models.blog_post.BlogPost
    :param kwargs: additional keyword arguments
    """
    if instance.slug is None:
        instance.slug = slugify(instance.title)
