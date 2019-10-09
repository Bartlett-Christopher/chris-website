# -*- coding: utf-8 -*-
"""
  :synopsis: view for contact page.

.. module: home.views.contact
.. author: Chris Bartlett <bartlett.christopher.p@gmail.com>
"""
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic.edit import FormView


class ContactView(FormView):
    """View for contact us."""

    form_class = ''
    template_name = 'home/contact.html'

    def form_valid(self, form):
        """Handle when submitted form is valid.

        Send email and redirect to thank you page.

        :param form: the submitted form
        :type form: home.forms.contact.ContactUsForm
        :return: a redirect to a thank you page
        :rtype: django.http.HttpResponse
        """
        form.send_email()
        return HttpResponseRedirect(reverse('home:thank-you'))
