# -*- encoding: utf8 -*-
from commons.helper.db_manager import DBManager
from dao.models.rights.user_token import UserToken


class UserTokenManager(DBManager):

    def __init__(self):
        super(DBManager, self).__init__()
        self.model = UserToken
        self.params = self.get_editable_fields()

    def verify_token(self, manager_id, token):
        if token is None:
            return False
        filter_conditions = {'manager_id': manager_id}
        token_obj = self.query_first(filter_conditions)
        return token_obj is not None or token_obj.token == token
