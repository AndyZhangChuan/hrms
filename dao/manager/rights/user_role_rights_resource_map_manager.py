# -*- encoding: utf8 -*-
from commons.helper.db_manager import DBManager
from dao.models.rights.user_role_rights_resource_map import UserRoleRightsResourceMap


class UserRoleRightsResourceMapManager(DBManager):

    def __init__(self):
        super(DBManager, self).__init__()
        self.model = UserRoleRightsResourceMap
        self.params = self.get_editable_fields()

    def get_resource_ids_by_role_ids(self, role_ids):
        expressions = [self.model.role_id.in_(role_ids), self.model.is_del == 0]
        resource_items = self.query(expressions=expressions)
        return [item.resource_id for item in resource_items]

    def allocate_rights_for_role(self, role_id, resource_ids):
        params_list = [{'role_id': role_id, 'resource_id': resource_id} for resource_id in resource_ids]
        return self.batch_create(params_list)

    def delete_by_resource_ids(self, resource_ids):
        expressions = [self.model.resource_id.in_(resource_ids)]
        models = self.query(expressions=expressions)
        self.batch_delete(models)
