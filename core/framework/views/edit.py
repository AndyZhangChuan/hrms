# -*- coding: utf-8 -*-

from flask import redirect

from core.framework.exceptions import ImproperlyConfigured
from core.framework.views.base import View, TemplateResponseMixin


class FormMixin(object):
    """
    A mixin that provides a way to show and handle a form in request.
    """
    form_class = None
    success_url = None

    def get_form_class(self):
        """
        Returns the form class to use in this view
        """
        return self.form_class

    def get_form(self, form_class=None):
        """
        Returns an instance of the form to be used in this view.
        """
        if form_class is None:
            form_class = self.get_form_class()
        return form_class()

    def get_context_data(self, **kwargs):
        """
        Insert the form into the context dict.
        """
        if 'form' not in kwargs:
            kwargs['form'] = self.get_form()
        return super(FormMixin, self).get_context_data(**kwargs)

    def get_success_url(self):
        if self.success_url:
            url = self.success_url
        else:
            raise ImproperlyConfigured(
                "No URL to redirect to. Provide a success_url.")
        return url

    def form_valid(self, form):
        return redirect(self.get_success_url())

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


class ProcessFormView(View):
    """
    A mixin that renders a form on GET and processes it on POST.
    """
    def get(self, *args, **kwargs):
        """
        Handles GET requests and instantiates a blank version of the form.
        """
        return self.render_to_response(self.get_context_data())

    def post(self, *args, **kwargs):
        """
        Handles POST requests, instantiating a form instance with the passed
        POST variables and then checked for validity.
        """
        form = self.get_form()
        if form.validate_on_submit():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class BaseFormView(FormMixin, ProcessFormView):
    """
    A base view for displaying a form
    """


class FormView(TemplateResponseMixin, BaseFormView):
    """
    A view for displaying a form, and rendering a template response.
    """
