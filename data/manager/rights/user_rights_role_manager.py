# -*- encoding: utf8 -*-
from commons.helper.db_manager import DBManager
from data.models.rights.user_rights_role import UserRightsRole


class UserRightsRoleManager(DBManager):

    def __init__(self):
        super(DBManager, self).__init__()
        self.model = UserRightsRole
        self.params = self.get_editable_fields()

    def check_role_exist(self, role_name, exclude_id=None):
        role = self.get_role_by_name(role_name)
        if role is None:
            return False
        return role.id != exclude_id

    def get_role_by_name(self, value):
        filter_conditions = {'role_name': value, 'is_del': 0}
        return self.query_first(filter_conditions)

    def get_roles_by_ids(self, role_ids):
        expressions = [self.model.id.in_(role_ids)]
        return self.query(expressions=expressions)