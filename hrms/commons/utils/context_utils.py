# -*- encoding: utf8 -*-

import threading

request_context = threading.local()


def get_request_context_data():
    return request_context.__dict__


def clear_request_context():
    request_context.__dict__.clear()

