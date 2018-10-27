# -*- encoding: utf8 -*-

from flask import request, jsonify
import re
from functools import wraps
from core import app
from commons.utils import web_util
from data.manager.rights import UserTokenMgr
from service.rights import rights_resource_service


def rights(resource_value):
    def rights_check(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            return f(*args, **kwargs)
            # 不进行权限控制的请求
            request_url = request.path
            exclude_url = app.config.get('RIGHTS_EXCLUDE_RESOURCE_LIST', None)
            for regPattern in exclude_url:
                if re.match(regPattern, request_url):
                    return f(*args, **kwargs)

            manager_id = web_util.get_operator_id_by_session()
            if manager_id == 0 and not _check_manager_token(manager_id, request.args.get('token', None)):
                return jsonify(status='error', msg='rights check error')

            # 这里后面使用redis缓存
            resources = rights_resource_service.get_manager_rights_list(manager_id)
            for resource in resources:
                if resource.value == resource_value:
                    return f(*args, **kwargs)

            return jsonify(status='error', msg='rights check error')

        return decorated_function
    return rights_check


def _check_manager_token(manager_id, token):
    return UserTokenMgr.verify_token(manager_id, token)