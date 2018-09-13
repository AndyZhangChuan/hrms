# -*- encoding: utf8 -*-
from commons.helper.db_manager import DBManager
from hrms.dao.models.rights.user_role_rights_resource_map import UserRoleRightsResourceMap


class UserRoleRightsResourceMapManager(DBManager):

    def __init__(self):
        super(DBManager, self).__init__()
        self.model = UserRoleRightsResourceMap
        self.params = self.get_editable_fields()

