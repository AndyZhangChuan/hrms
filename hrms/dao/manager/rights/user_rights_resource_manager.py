# -*- encoding: utf8 -*-
from commons.helper.db_manager import DBManager
from hrms.dao.models.rights.user_rights_resource import UserRightsResource


class UserRightsResourceManager(DBManager):

    def __init__(self):
        super(DBManager, self).__init__()
        self.model = UserRightsResource
        self.params = self.get_editable_fields()
