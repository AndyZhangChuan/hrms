# -*- encoding: utf8 -*-

from dao.manager.rights import UserRoleRightsResourceMapMgr
from dao.manager.rights import UserRightsRoleMapMgr
from dao.manager.rights import UserRightsResourceMgr


def get_manager_rights_list(manager_id):
    role_ids = UserRightsRoleMapMgr.get_user_role_ids(manager_id)
    if len(role_ids) == 0:
        return []
    resource_ids = UserRoleRightsResourceMapMgr.get_resource_ids_by_role_ids(role_ids)
    if len(resource_ids) == 0:
        return []
    return UserRightsResourceMgr.get_resource_by_ids(resource_ids)

