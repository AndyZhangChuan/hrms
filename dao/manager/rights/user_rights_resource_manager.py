# -*- encoding: utf8 -*-
from commons.helper.db_manager import DBManager
from dao.models.rights import UserRightsResource


class UserRightsResourceManager(DBManager):

    def __init__(self):
        super(DBManager, self).__init__()
        self.model = UserRightsResource
        self.params = self.get_editable_fields()
