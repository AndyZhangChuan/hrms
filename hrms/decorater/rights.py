# -*- encoding: utf8 -*-

from flask import request, session
import re
from functools import wraps
from core import app, db


def rights_check(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):

        # 不进行权限控制的请求
        request_url = request.path
        exclude_url = app.config.get('RIGHTS_EXCLUDE_URL_REGPATTERN', None)
        for regPattern in exclude_url:
            if re.match(regPattern, request_url):
                return f(*args, **kwargs)

        # 权限当前登录的用户是否有action的访问权限
        userid = session.get('crm_user_id')
        rights_key = 'crm_rights_key_' + str(userid)
        resources = ''
        if 'CRM_RIGHTS_REDIS' in app.config.keys() and app.config.get('CRM_RIGHTS_REDIS'):
            resources = redis.get(rights_key)
            if resources:
                resources = eval(resources)
        if not resources:
            userRoles = UserRoleMap.query.filter(UserRoleMap.user_id == userid, UserRoleMap.del_flag == 0, ).all()
            roleIds = [userRole.role_id for userRole in userRoles]
            roleResourceMaps = RoleResourceMap.query.filter(RoleResourceMap.role_id.in_(roleIds),
                                                            RoleResourceMap.del_flag == 0).all()
            resourceIds = [roleResourceMap.resource_id for roleResourceMap in roleResourceMaps]
            resources = db.session.query(Resource.value).filter(Resource.id.in_(resourceIds),
                                                                Resource.del_flag == 0).all()
            # 为提高性能，后续可将账号对应的权限缓存至redis
            if 'CRM_RIGHTS_REDIS' in app.config.keys() and app.config.get('CRM_RIGHTS_REDIS'):
                redis.set(rights_key, resources)
                redis.expire(rights_key, 600)
                print 'redis for rights check init - ' + str(userid)
                print resources
        for resource in resources:
            reses = resource[0].split(";")
            for res in reses:
                if re.match(res, request_url):
                    return f(*args, **kwargs)

        return redirect(url_for('forbid'))

    return decorated_function
