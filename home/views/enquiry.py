# -*- coding: utf-8 -*-
"""
  :synopsis: view for enquiry page.

.. module: home.views.enquiry
.. author: Chris Bartlett <bartlett.christopher.p@gmail.com>
"""
from django.views.generic.edit import FormView

from home.forms import EnquiryForm


class EnquiryView(FormView):
    """View for contact us."""

    form_class = EnquiryForm
    template_name = 'home/enquiry.html'

    def form_valid(self, form):
        """
        Save the form and re-render the contact-us page with the result.

        :param form: the enquiry form
        :type form: home.forms.enquiry.EnquiryForm
        :return: the successful enquiry response
        :rtype: django.http.HttpResponse
        """
        instance = form.save(commit=True)
        extra_context = {
            'enquiry': instance,
            'request_received': True,
        }
        return self.render_to_response(
            self.get_context_data(**extra_context)
        )
