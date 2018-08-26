# -*- encoding: utf8 -*-

from flask import request


def get_operator_id():
    return int(request.headers.get("User-Id", 0))