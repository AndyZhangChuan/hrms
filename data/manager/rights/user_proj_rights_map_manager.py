# -*- encoding: utf8 -*-
from commons.helper.db_manager import DBManager
from data.models.rights.user_proj_rights_map import UserProjRightsMap


class UserProjRightsMapManager(DBManager):

    def __init__(self):
        super(DBManager, self).__init__()
        self.model = UserProjRightsMap
        self.params = self.get_editable_fields()

