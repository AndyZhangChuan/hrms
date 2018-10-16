# -*- encoding: utf8 -*-
from flask import request


def get_request_proj_id():
    id = request.headers.get('proj_id')
    return int(id) if id else 0
