# -*- encoding: utf8 -*-
from commons.helper.db_manager import DBManager
from dao.models.rights.user_rights_role_map import UserRightsRoleMap


class UserRightsRoleMapManager(DBManager):

    def __init__(self):
        super(DBManager, self).__init__()
        self.model = UserRightsRoleMap
        self.params = self.get_editable_fields()

    def get_user_role_ids(self, manager_id):
        filter_conditions = {'manager_id': manager_id, 'is_del': 0}
        role_map_items = self.query(filter_conditions=filter_conditions)
        return [item.role_id for item in role_map_items]

    def allocate_roles_for_manager(self, manager_id, role_ids):
        params_list = [{'manager_id': manager_id, 'role_id': role_id} for role_id in role_ids]
        return self.batch_create(params_list)

    def delete_by_role_ids(self, role_ids):
        expressions = [self.model.role_id.in_(role_ids)]
        models = self.query(expressions=expressions)
        return self.batch_delete(models)