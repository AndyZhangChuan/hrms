# -*- coding: utf-8 -*-

import json

from flask import make_response

from core.framework.views.base import View, ContextMixin
from core.framework.views.edit import BaseFormView


__all__ = [
    'JsonResponseMixin',
    'JsonView',
    'JsonFormView',
]


class JsonResponseMixin(object):
    """
    A mixin that can be used to return json for api view.
    """

    status = 'ok'
    error_code = 0
    error_msg = 'message'

    def update_errors(self, msg, error_code=1):
        self.status = 'fail'
        self.error_code = error_code
        self.error_msg = msg

    def render_to_response(self, data=None):
        context = {
            'status': self.status
        }
        if self.error_code:
            context.update({
                'errorCode': self.error_code,
                'errorMsg': self.error_msg
            })
        if data is None:
            data = {}
        context.update({
            'content': data
        })

        response = make_response(json.dumps(context))
        response.headers['Content-Type'] = 'application/json'

        return response


class JsonView(JsonResponseMixin, ContextMixin, View):
    """
    A view that return json format response.
    """

    def get(self, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)


class JsonFormView(JsonResponseMixin, BaseFormView):
    """
    A view for process form and return json format response.
    """
    def form_valid(self, form):
        return self.render_to_response(form.data)

    def form_invalid(self, form):
        error = form.errors.popitem()[-1][0]
        self.update_errors(error)
        return self.render_to_response()
