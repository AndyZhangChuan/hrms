# -*- encoding: utf8 -*-

import json
from dao.manager.rights import ManagerMgr
from dao.manager.rights import UserRightsRoleMapMgr
from dao.manager.rights import UserRightsRoleMgr
from dao.manager.rights import UserProjRightsMapMgr
from dao.manager.proj import ProjMgr
from commons.utils import page_util
from commons.utils import to_dict
from commons.utils import md5_utils


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
    filter_conditions = {'user_status': 1, 'email': form.email.data}
    manager = ManagerMgr.query_first(filter_conditions=filter_conditions)
    if not manager or manager.email != form.email.data:
        return dict(status='error', msg='用户名或密码失败')

    # 刷新token
    token = md5_utils.generate_random_md5_str()

    data = {
        'status': 'ok',
        'content': {
            "user_id": manager.id,
            "user_name": manager.user_name,
            "phone": manager.phone
        },
        "token": token
    }
    return data


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
