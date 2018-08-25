# -*- coding: utf-8 -*-

from flask import redirect
from flask import make_response
from flask import render_template
from flask.views import MethodView

from core.framework.exceptions import ImproperlyConfigured


__all__ = [
    'View',
    'ContextMixin',
    'TemplateResponseMixin',
    'TemplateView',
    'RedirectView',
]


class View(MethodView):
    """
    Intentionally simple parent class for all views.
    """


class ContextMixin(object):
    """

    A default context mixin that passes an empty dict.
    """

    def get_context_data(self, **kwargs):
        return {}


class TemplateResponseMixin(object):
    """
    A mixin that can be used to render a template.
    """
    template_name = None

    def render_to_response(self, context):
        """
        Returns a responsewith a template rendered with the
        given context.
        """
        return render_template(self.get_template_names(), **context)

    def get_template_names(self):
        """
        Returns a list of template names to be used for the request. Must return
        a list. May not be called if render_to_response is overridden.
        """
        if self.template_name is None:
            raise ImproperlyConfigured(
                "TemplateResponseMixin requires either a definition of "
                "'template_name' or an implementation of 'get_template_names()'")
        else:
            return [self.template_name]


class TemplateView(TemplateResponseMixin, ContextMixin, View):
    """
    A view that renders a template.  This view will also pass into the context
    any keyword arguments passed by the URLconf.
    """
    def get(self, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)


class RedirectView(View):
    """
    A view that provides a redirect on any GET request.
    """
    permanent = False
    url = None
    __HTTP_REDIRECT_CODE = {
        'permanent': 301,
        'temporary': 302
    }

    def get_redirect_url(self, **kwargs):
        """
        Return the URL redirect to.
        """
        return self.url % kwargs

    def get(self, *args, **kwargs):
        url = self.get_redirect_url(**kwargs)
        if url:
            if self.permanent:
                code = self.__HTTP_REDIRECT_CODE['permanent']
            else:
                code = self.__HTTP_REDIRECT_CODE['temporary']
            return redirect(url, code)
        else:
            response = make_response('Redirect url is None', 410)
            return response

    def head(self, *args, **kwargs):
        return self.get(*args, **kwargs)

    def post(self, *args, **kwargs):
        return self.get(*args, **kwargs)

    def options(self, *args, **kwargs):
        return self.get(*args, **kwargs)

    def delete(self, *args, **kwargs):
        return self.get(*args, **kwargs)

    def put(self, *args, **kwargs):
        return self.get(*args, **kwargs)

    def patch(self, *args, **kwargs):
        return self.get(*args, **kwargs)
