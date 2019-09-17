# -*- coding: utf-8 -*-
"""
.. module:: staticpages.models.staticpage
   :synopsis: Model to describe a static web page

.. moduleauthor:: Chris Bartlett <chris.bartlett@therealbuzzgroup.com>
"""
from ckeditor import fields

from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _

from common.mixins import EnabledMixin, TimeStampMixin


class StaticPage(TimeStampMixin, EnabledMixin, models.Model):
    """
    Model to describe a static web page
    """
    url = models.CharField(
        verbose_name=_('URL'),
        max_length=255,
        db_index=True,
        unique=True,
        help_text=_(
            'The relative url path describing what page this model represents.'
            'e.g. /about/'
        )
    )
    title = models.CharField(
        verbose_name=_('Title'),
        max_length=255,
        help_text=_('The page title')
    )
    content = fields.RichTextField(
        verbose_name=_('Content'),
        blank=True,
        null=True,
        help_text=_('The content to be displayed on the static page.')
    )
    template_name = models.CharField(
        verbose_name=_('Template name'),
        max_length=255,
        blank=True,
        null=True,
        help_text=_(
            'The relative path describing which template to use. If not set '
            'will default to /staticpages/page.html'
        )
    )

    class Meta:
        """ Metadata for StaticPage model """
        app_label = 'staticpages'
        verbose_name = _('Static page')
        verbose_name_plural = _('Static pages')

    @classmethod
    def get_page(cls, url):
        """
        Get the StaticPage object provided a url

        :param url: static page url
        :type url: str
        :return: the StaticPage or None
        :rtype: staticpages.models.staticpage.StaticPage or NoneType
        """
        try:
            cls.objects.get(url=url)
        except cls.DoesNotExist:
            return None


@receiver(pre_save, sender=StaticPage)
def sanitise_static_page_url(sender, instance, **kwargs):
    """
    Append '/' to end of URLs for Django
    :param sender:
    :param instance:
    :param kwargs:
    :return:
    """
    pass
