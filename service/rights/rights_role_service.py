# -*- encoding: utf8 -*-

from data.manager.rights import UserRightsRoleMgr
from data.manager.rights import UserRightsRoleMapMgr
from data.manager.rights import UserRoleRightsResourceMapMgr
from data.manager.rights import UserRightsResourceMgr
from commons.utils import page_util
from commons.utils import to_dict


def add_rights_role(form):
    params = {
        'role_name': form.role_name.data
    }
    if UserRightsRoleMgr.check_role_exist(params['role_name']):
        return dict(status='error', msg='已存在相同角色名称')
    if not UserRightsRoleMgr.create(**params):
        return dict(status='error', msg='角色创建失败')
    return dict(status='ok')


def update_rights_role(form):
    params = {
        'role_name': form.role_name.data
    }

    role = UserRightsRoleMgr.get(form.id.data)
    if role is None:
        return dict(status='error', msg='无效的角色编号')

    if UserRightsRoleMgr.check_role_exist(params['role_name'], role.id):
        return dict(status='error', msg='重复的角色名称')
    if not UserRightsRoleMgr.update(role, **params):
        return dict(status='error', msg='角色更新失败')
    return dict(status='ok')


def delete_rights_role(role_id):
    resource = UserRightsRoleMgr.get(role_id)
    if resource is None:
        return dict(status='error', msg='要删除的权限不存在')
    filter_conditions = {"role_id": role_id, 'is_del': 0}
    if UserRightsRoleMapMgr.query_first(filter_conditions):
        return dict(status='error', msg='有用户和此角色关联，无法删除')

    map_items = UserRoleRightsResourceMapMgr.query(filter_conditions)
    if len(map_items) > 0:
        UserRoleRightsResourceMapMgr.batch_delete(map_items)

    if UserRightsRoleMapMgr.delete(resource):
        return dict(status='ok')

    return dict(status='error', msg='权限删除成功')


def get_rights_role_list(page):
    order_by_list = [UserRightsRoleMgr.model.id.desc()]
    expressions = [UserRightsRoleMgr.model.is_del == 0]
    return page_util.get_page_result(UserRightsRoleMgr.model, page=page, expressions=expressions, page_size=10,
                                     order_by_list=order_by_list)


def get_rights_role_detail(role_id):
    role = UserRightsRoleMgr.get(role_id)
    if not role:
        return dict(status='error', msg='角色不存在')

    resource_ids = UserRoleRightsResourceMapMgr.get_resource_ids_by_role_ids([role_id])
    if len(resource_ids) == 0:
        rights_resource = []
    else:
        rights_resource = to_dict(UserRightsResourceMgr.get_resource_by_ids(resource_ids))
    data = {
        'status': 'ok',
        'content': {
            'basic': to_dict(role),
            'rights_resource': rights_resource
        }
    }
    return data


def rights_role_resource_allocate(role_id, rights_ids):
    role = UserRightsRoleMgr.get(role_id)
    if not role:
        return dict(status='error', msg='角色不存在')
    if len(UserRightsResourceMgr.get_resource_by_ids(rights_ids)) != len(rights_ids):
        return dict(status='error', msg='无效的权限编号')

    exist_resource_ids = UserRoleRightsResourceMapMgr.get_resource_ids_by_role_ids([role_id])
    remove_resource_ids = list(set(exist_resource_ids) - set(rights_ids))
    if len(remove_resource_ids) > 0:
        UserRoleRightsResourceMapMgr.delete_by_resource_ids(remove_resource_ids)

    final_rights_ids = list(set(rights_ids) - set(exist_resource_ids))
    if len(final_rights_ids) > 0:
        UserRoleRightsResourceMapMgr.allocate_rights_for_role(role_id, final_rights_ids)
    return dict(status='ok')


