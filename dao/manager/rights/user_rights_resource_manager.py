# -*- encoding: utf8 -*-
from commons.helper.db_manager import DBManager
from dao.models.rights.user_rights_resource import UserRightsResource


class UserRightsResourceManager(DBManager):

    def __init__(self):
        super(DBManager, self).__init__()
        self.model = UserRightsResource
        self.params = self.get_editable_fields()

    def get_resource_by_ids(self, ids):
        expressions = [self.model.id.in_(ids)]
        return self.query(expressions=expressions)
