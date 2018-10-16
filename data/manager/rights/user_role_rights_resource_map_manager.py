# -*- encoding: utf8 -*-
from commons.helper.db_manager import DBManager
from data.models.rights.user_role_rights_resource_map import UserRoleRightsResourceMap


class UserRoleRightsResourceMapManager(DBManager):

    def __init__(self):
        super(DBManager, self).__init__()
        self.model = UserRoleRightsResourceMap
        self.params = self.get_editable_fields()

    def get_resource_ids_by_role_ids(self, role_ids):
        expressions = [self.model.role_id.in_(role_ids)]
        resource_items = self.query(expressions=expressions)
        return [item.resource_id for item in resource_items]
