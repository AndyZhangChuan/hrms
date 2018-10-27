# -*- encoding: utf8 -*-

import json
import random
from core import app, redis
from data.manager.rights import ManagerMgr
from data.manager.rights import UserRightsRoleMapMgr
from data.manager.rights import UserRightsRoleMgr
from data.manager.rights import UserProjRightsMapMgr
from data.manager.rights import UserTokenMgr
from data.manager.proj import ProjMgr
from commons.utils import page_util
from commons.utils import to_dict
from commons.utils import md5_utils
from commons.constants import RightUserConstant
from commons.constants import CommonConstant
from commons.utils import time_util
from commons.sms import sms_service
from commons.exception import ValidationError


def add_manager(form):
    params = {
        'user_name': form.user_name.data,
        'phone': form.phone.data,
        'email': form.email.data
    }

    if ManagerMgr.check_exist_by_email_phone(params['email'], params['phone']):
        return dict(status='error', msg='邮箱或电话号码已经存在')
    if ManagerMgr.create(**params):
        return dict(status='ok')
    return dict(status='error', msg='新增用户失败')


def update_manager(form):
    params = {
        'user_name': form.user_name.data,
        'phone': form.phone.data,
        'email': form.email.data,
        'user_status': form.email.user_status
    }
    manager = ManagerMgr.get(form.id.data)
    if manager is None:
        return dict(status='error', msg='用户不存在')
    if ManagerMgr.update(manager, **params):
        return dict(status='ok')
    return dict(status='error', msg='用户更新失败')


def get_manager_list(page):
    order_by_list = [ManagerMgr.model.id.desc()]
    expressions = [ManagerMgr.model.is_del == 0]
    return page_util.get_page_result(ManagerMgr.model, page=page, expressions=expressions, page_size=10,
                                     order_by_list=order_by_list)


def get_manager_detail(manager_id):
    manager = ManagerMgr.get(manager_id)
    if manager is None:
        return dict(status='error', msg='用户不存在')
    basic = to_dict(manager)
    role_ids = UserRightsRoleMapMgr.get_user_role_ids([manager_id])
    roles = UserRightsRoleMgr.get_roles_by_ids(role_ids)
    proj_rights_list = UserProjRightsMapMgr.get_rights_by_manager_id(manager_id)
    company_rights = [item.company_id for item in proj_rights_list if item.proj_id == 0]
    proj_rights = [{'company_id': item.company_id, 'proj_id': item.proj_id} for item in proj_rights_list if item.proj_id == 0]
    data = {
        'status': 'ok',
        'content': {
            'basic': basic,
            'roles': to_dict(roles),
            'proj_rights': {
                'company_rights': company_rights,
                'proj_rights': proj_rights
            }
        }
    }
    return data


def manager_login(form):
    """
    使用手机号登陆
    :return:
    """
    try:
        filter_conditions = {'user_status': 1, 'email': form.phone.data}
        manager = ManagerMgr.query_first(filter_conditions=filter_conditions)
        if not manager or manager.email != form.email.data:
            return dict(status='error', msg='用户名或密码失败')

        # 验证登录
        data = _validate_login_sms_code(form.phone.data, form.code.data)
        if data['status'] != 'ok':
            return {"status": "error", "msg": data['message']}

        # 刷新token
        token = md5_utils.generate_random_md5_str()
        user_token = UserTokenMgr.get_token(manager.id)
        if user_token:
            UserTokenMgr.update(user_token, token=token)
        else:
            UserTokenMgr.create(manager_id=manager.id, token=token)

        data = {
            'status': 'ok',
            'content': {
                "user_id": manager.id,
                "user_name": manager.user_name,
                "phone": manager.phone
            },
            "token": token
        }
        return {'status': 'ok', 'data': data}
    except Exception, ex:
        print ex
        raise ValidationError('登陆验证失败')


def _validate_login_sms_code(phone, code):
    """
    校验商城登录短信验证码
    :param phone: 手机号
    :param code:  验证码
    :return:
    """
    key = "%s:%d" % (app.config.get("MANAGER_LOGIN_MSG_CODE"), int(phone))
    auth_count_key = "AUTH_COUNT_{0}:{1}".format(app.config.get("MANAGER_LOGIN_MSG_CODE"), int(phone))
    redis_code = redis.get(key)
    redis.incr(auth_count_key, 1)
    if int(redis.get(auth_count_key)) > 10:
        return dict(status='error', message='短信验证次数过多')
    if code and redis_code:
        if int(redis_code) == int(code):
            return dict(status='ok')
    return dict(status='error', message='验证码错误')


def manager_role_allocate(manager_id, role_ids):
    manager = ManagerMgr.get(manager_id)
    if not manager:
        return dict(status='error', msg='用户不存在')
    if len(UserRightsRoleMgr.get_roles_by_ids(role_ids)) != len(role_ids):
        return dict(status='error', msg='无效的角色编号')
    exist_role_ids = UserRightsRoleMapMgr.get_user_role_ids(manager_id)
    remove_role_ids = list(set(exist_role_ids) - set(role_ids))
    if len(remove_role_ids) > 0:
        UserRightsRoleMapMgr.delete_by_role_ids(remove_role_ids)
    final_role_ids = list(set(role_ids) - set(exist_role_ids))
    if len(final_role_ids) > 0:
        UserRightsRoleMapMgr.allocate_roles_for_manager(manager_id, final_role_ids)
    return dict(status='ok')


def manager_proj_rights_allocate(form):
    manager_id = form.manager_id.data
    proj_map = form.proj_map.data
    manager = ManagerMgr.get(manager_id)
    if not manager:
        return dict(status='error', msg='用户不存在')
    proj_dict = json.loads(proj_map)
    UserProjRightsMapMgr.delete_rights_by_manager_id(manager_id)
    if proj_dict.get('proj_ids', None):
        return __allocate_proj_rights_by_proj(manager_id, proj_dict['proj_ids'])
    elif proj_dict.get('company_ids'):
        return __allocate_proj_rights_by_company(manager_id, proj_dict['company_ids'])
    return dict(status='error', msg='无效的项目数据结构')


def send_login_auth_code(phone):
    """
    使用手机号发送登录验证码
    安全策略：
    1. 保证微信端登陆，session存在open_id
    2. 每个phone 每两个小时只能发送5次
    3. 每个号码 每天只能发送15次
    4. 每个openid 每天只能发送15次
    5. 出现步骤4这种情况则对open_id进行封号一年
    :param phone:
    :return:
    """
    # 1.确保非跨域
    pass

    # 2.检查是否已经被封号
    switch_key = _get_login_code_switch_key(phone)
    if redis.get(switch_key) == RightUserConstant.LOGIN_VERIFY_CODE_SWITCH_CLOSED:
        return dict(status='error', msg='您由于恶意操作已被封号，请联系管理员!')

    # 3.每个phone 每两个小时只能发送5次
    hour_verify_result = _verify_hour_code_count(phone)
    if hour_verify_result['status'] != 'ok':
        return hour_verify_result

    # 4.每个号码每天只能发送15次，4.每个openid 每天只能发送15次
    daily_verify_result = _verify_daily_code_count(phone)
    if daily_verify_result['status'] != 'ok':
        return daily_verify_result

    sms_service.send_login_code(phone, _get_login_auth_code(phone))
    return dict(status='ok')


def _get_login_auth_code(phone):
    """
    使用手机号获得登录验证码
    :param phone:
    :return:
    """
    key = "%s:%d" % (app.config.get("MANAGER_LOGIN_MSG_CODE"), int(phone))
    auth_count_key = "AUTH_COUNT_{0}:{1}".format(app.config.get("MANAGER_LOGIN_MSG_CODE"), int(phone))
    if redis.exists(key):
        code = int(redis.get(key))
    else:
        code = int(random.uniform(1000, 9999))
        redis.set(key, code)
        redis.expire(key, 15*60)
        redis.set(auth_count_key, 0)
        redis.expire(auth_count_key, 15*60)
    return code


def _verify_hour_code_count(phone):
    """
    校验每小时发送频次（这里主要校验每两个小时发送次数不能超过5次）
    :param phone:
    :return:
    """
    message_count_key = _get_message_hour_count_key(phone)
    message_count = redis.get(message_count_key)
    if message_count and int(message_count) >= RightUserConstant.LOGIN_CODE_SEND_TWO_HOUR_LIMIT:
        return dict(status='error', msg='短信发送过多, 请2小时后再重试!')

    redis.incr(message_count_key, 1)
    redis.expire(message_count_key, CommonConstant.ONE_HOUR_TIMESTAMP * 2)
    return dict(status='ok')


def _verify_daily_code_count(phone):
    """
    校验每天发送频次不能超过15次
    :param phone:
    :return:
    """
    date_str = time_util.currentDateString()
    open_message_count_key = _get_daily_message_count_key(phone, date_str)
    phone_message_count_key = _get_daily_message_count_key(phone, date_str)

    result = True

    # 每个号码每天的次数不能超过15次
    phone_message_count = redis.get(phone_message_count_key)
    if phone_message_count and int(phone_message_count) > RightUserConstant.LOGIN_CODE_SEND_DAY_LIMIT:
        result = False
    redis.incr(phone_message_count_key, 1)
    redis.expire(phone_message_count_key, CommonConstant.ONE_DAY_TIMESTAMP)

    # 每个phone 次数不能超过15次, 超过则封号
    open_message_count = redis.get(open_message_count_key)
    if open_message_count and int(open_message_count) > RightUserConstant.LOGIN_CODE_SEND_DAY_LIMIT:
        switch_key = _get_login_code_switch_key(phone)
        redis.setex(switch_key, RightUserConstant.LOGIN_VERIFY_CODE_SWITCH_CLOSED,
                    CommonConstant.ONE_DAY_TIMESTAMP * 365)

        # TODO 打印errorLog 配置预警监控

        result = False

    redis.incr(open_message_count_key, 1)
    redis.expire(open_message_count_key, CommonConstant.ONE_DAY_TIMESTAMP)

    if not result:
        return dict(status='error', msg='超过每日发送限制')

    return dict(status='ok')


def _get_login_code_switch_key(phone):
    return "{0}_{1}_switch:{2}".format(RightUserConstant.MESSAGE_DAILY_COUNT_REDIS_KEY_PREFIX,
                                       app.config.get("MANAGER_LOGIN_MSG_CODE"),
                                       phone)


def _get_message_hour_count_key(phone):
    return "{0}_{1}:{2}".format(RightUserConstant.MESSAGE_COUNT_REDIS_KEY_PREFIX,
                                app.config.get("MANAGER_LOGIN_MSG_CODE"),
                                phone)


def _get_daily_message_count_key(key, date_str):
    return "{0}_{1}_{2}:{3}".format(RightUserConstant.MESSAGE_DAILY_COUNT_REDIS_KEY_PREFIX,
                                    app.config.get("MANAGER_LOGIN_MSG_CODE"),
                                    date_str,
                                    key)


def __allocate_proj_rights_by_proj(manager_id, proj_ids):
    projs = ProjMgr.get_proj_by_ids(proj_ids)
    params_list = [{'company_id': proj.company_id, 'proj_id': proj.id} for proj in projs]
    if UserProjRightsMapMgr.allocate_rights_by_company_proj_list(manager_id, params_list):
        return dict(status='ok')
    return dict(status='error', msg='项目级别权限分配失败')


def __allocate_proj_rights_by_company(manager_id, company_ids):
    if UserProjRightsMapMgr.allocate_rights_by_company_ids(manager_id, company_ids):
        return dict(status='ok')
    return dict(status='error', msg='公司级别权限分配失败')

