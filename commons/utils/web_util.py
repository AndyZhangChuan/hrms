# -*- encoding: utf8 -*-

from flask import request, session


def get_operator_id():
    operator_id = get_operator_id_by_session() == 0
    if operator_id != 0:
        return operator_id
    return int(request.headers.get("User-Id", 0))


def get_operator_id_by_session():
    if session.get('login_manager_id'):
        return session['login_manager_id']
    return 0

