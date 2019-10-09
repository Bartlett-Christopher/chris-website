# -*- coding: utf-8 -*-
"""
  :synopsis: view for contact page.

.. module: home.views.contact
.. author: Chris Bartlett <bartlett.christopher.p@gmail.com>
"""
from django.views.generic.edit import FormView

from home.forms import ContactUsForm


class ContactUsView(FormView):
    """View for contact us."""

    form_class = ContactUsForm
    template_name = 'home/contact_us.html'

    def form_valid(self, form):
        form.send_email()
        return self.render_to_response(
            self.get_context_data(request_received=True)
        )
