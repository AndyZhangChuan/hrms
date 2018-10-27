# -*- encoding: utf8 -*-

from data.manager.rights import UserRoleRightsResourceMapMgr
from data.manager.rights import UserRightsRoleMapMgr
from data.manager.rights import UserRightsResourceMgr
from commons.utils import page_util
from commons.utils import to_dict


def get_manager_rights_list(manager_id):
    role_ids = UserRightsRoleMapMgr.get_user_role_ids(manager_id)
    if len(role_ids) == 0:
        return []
    resource_ids = UserRoleRightsResourceMapMgr.get_resource_ids_by_role_ids(role_ids)
    if len(resource_ids) == 0:
        return []
    return UserRightsResourceMgr.get_resource_by_ids(resource_ids)


def add_rights_resource(form):
    params = {
      'resource_name': form.resource_name.data,
      'value': form.value.data,
      'resource_type': form.resource_type.data,
      'parent_id': form.parent_id.data,
      'rank': form.rank.data
    }
    if params['parent_id'] != 0 and not UserRightsResourceMgr.get(params['parent_id']):
        return dict(status='error', msg='无效的父权限编号')
    if UserRightsResourceMgr.check_resource_exist(params['value']):
        return dict(status='error', msg='资源已经创建')
    if UserRightsResourceMgr.create(**params) is None:
        return dict(status='error', msg='权限创建失败')
    return dict(status='ok')


def update_rights_resource(form):
    params = {
        'resource_name': form.resource_name.data,
        'value': form.value.data,
        'resource_type': form.resource_type.data,
        'parent_id': form.parent_id.data,
        'rank': form.rank.data
    }
    if params['parent_id'] != 0 and not UserRoleRightsResourceMapMgr.get(params['parent_id']):
        return dict(status='error', msg='无效的父权限编号')

    resource = UserRightsResourceMgr.get(form.id.data)
    if resource is None:
        return dict(status='error', msg='要创建的权限不存在')

    if UserRightsResourceMgr.check_resource_exist(params['value'], resource.id):
        return dict(status='error', msg='资源已经创建')

    if UserRightsResourceMgr.update(resource, **params):
        return dict(status='ok')
    return dict(status='error', msg='权限更新错误')


def delete_rights_resource(resource_id):
    resource = UserRightsResourceMgr.get(resource_id)
    if resource is None:
        return dict(status='error', msg='要删除的权限不存在')
    filter_conditions = {"resource_id": resource_id, 'is_del': 0}
    if UserRoleRightsResourceMapMgr.query_first(filter_conditions):
        return dict(status='error', msg='有角色和此权限关联，无法删除')
    if UserRightsResourceMgr.delete(resource):
        return dict(status='ok')
    return dict(status='error', msg='权限删除成功')


def get_rights_resource_list(page):
    order_by_list = [UserRightsResourceMgr.model.id.desc()]
    expressions = [UserRightsResourceMgr.model.is_del == 0]
    return page_util.get_page_result(UserRightsResourceMgr.model, page=page, expressions=expressions, page_size=10,
                                     order_by_list=order_by_list)


def get_rights_resource_list_by_parent_id(parent_id):
    expressions = [UserRightsResourceMgr.model.is_del == 0, UserRightsResourceMgr.model.parent_id == parent_id]
    return page_util.get_page_result(UserRightsResourceMgr.model, page=1, expressions=expressions, page_size=0)


def get_rights_resource_detail(resource_id):
    resource = UserRightsResourceMgr.get(resource_id)
    if resource is None:
        return dict(status='error', msg='权限不存在')
    return dict(status='ok', content=to_dict(resource))


def get_rights_tree():
    resources = UserRightsResourceMgr.query(filter_conditions={'is_del': 0})
    group = [resource.id for resource in resources if resource.parent_id == 0]
    group_child_map = dict()
    for group_id in group:
        group_child_map[group_id] = [resource.id for resource in resources if resource.parent_id == group_id]
    detail = [{resource.id: to_dict(resource)} for resource in resources]

    data = {
        'status': 'ok',
        'content': {
            'group': group,
            'group_child_map': group_child_map,
            'detail': detail
        }
    }
    return data
