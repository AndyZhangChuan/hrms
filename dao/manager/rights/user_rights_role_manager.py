# -*- encoding: utf8 -*-
from commons.helper.db_manager import DBManager
from dao.models.rights.user_rights_role import UserRightsRole


class UserRightsRoleManager(DBManager):

    def __init__(self):
        super(DBManager, self).__init__()
        self.model = UserRightsRole
        self.params = self.get_editable_fields()
