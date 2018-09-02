# -*- encoding: utf8 -*-
from commons.helper.db_manager import DBManager
from hrms.dao.models.rights.user_token import UserToken


class UserTokenManager(DBManager):

    def __init__(self):
        super(DBManager, self).__init__()
        self.model = UserToken
        self.params = self.get_editable_fields()

