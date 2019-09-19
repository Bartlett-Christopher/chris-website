# -*- coding: utf-8 -*-
"""
.. module:: staticpages.models.page
   :synopsis: Model to describe a static web page

.. moduleauthor:: Chris Bartlett <chris.bartlett@therealbuzzgroup.com>
"""
from ckeditor import fields

from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _

from common.mixins import EnabledMixin, TimeStampMixin
from staticpages.exceptions import PageNotFound


class Page(TimeStampMixin, EnabledMixin, models.Model):
    """ Model to describe a static web page """
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
        verbose_name = _('Page')
        verbose_name_plural = _('Pages')

    @classmethod
    def get_page(cls, url):
        """
        Get the Page object provided a url

        :param url: static page url
        :type url: str
        :return: the Page
        :rtype: staticpages.models.page.Page
        :raises: staticpages.exceptions.PageNotFound
        """
        clean_url = cls.process_url(url)
        try:
            page = cls.objects.get(url=clean_url)
        except cls.DoesNotExist:
            raise PageNotFound

        return page

    @staticmethod
    def process_url(url):
        """
        Process the static page URL ensuring it starts and ends with '/'

        :param url: the provided static page URL
        :type url: str
        :return: the final static page URL with starting and trailing '/'
        """
        if not url.startswith('/'):
            url = '/' + url

        if not url.endswith('/'):
            url += '/'

        return url



@receiver(pre_save, sender=Page)
def pre_save_static_page(sender, instance, **kwargs):
    """
    Pre-save signal handler for Page model
    - append '/' to start and end of URLs (if necessary) for Django
    - set the default template name if none given

    :param sender: sender class
    :type sender: staticpages.models.page.Page
    :param instance: model instance being saved
    :type sender: staticpages.models.page.Page
    :param kwargs: not used
    """
    instance.url = sender.process_url(instance.url)

    if instance.template_name is None:
        # we are not specifying a template override, set default
        instance.template_name = 'staticpages/page.html'

