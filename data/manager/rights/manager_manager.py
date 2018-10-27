# -*- encoding: utf8 -*-
from commons.helper.db_manager import DBManager
from data.models.rights.manager import Manager
from sqlalchemy import or_


class ManagerManager(DBManager):

    def __init__(self):
        super(DBManager, self).__init__()
        self.model = Manager
        self.params = self.get_editable_fields()

    def check_exist_by_email_phone(self, email, phone):
        expressions = [or_(self.model.email == email, self.model.phone == phone)]
        filter_conditions = {'is_del': 0}
        self.query_first(filter_conditions=filter_conditions, expressions=expressions)
