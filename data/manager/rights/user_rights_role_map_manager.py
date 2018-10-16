# -*- encoding: utf8 -*-
from commons.helper.db_manager import DBManager
from data.models.rights.user_rights_role_map import UserRightsRoleMap


class UserRightsRoleMapManager(DBManager):

    def __init__(self):
        super(DBManager, self).__init__()
        self.model = UserRightsRoleMap
        self.params = self.get_editable_fields()

    def get_user_role_ids(self, manager_id):
        filter_conditions = {'manager_id': manager_id}
        role_map_items = self.query(filter_conditions=filter_conditions)
        return [item.role_id for item in role_map_items]
