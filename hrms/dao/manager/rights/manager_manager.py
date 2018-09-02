# -*- encoding: utf8 -*-
from commons.helper.db_manager import DBManager
from hrms.dao.models.rights.manager import Manager


class ManagerManager(DBManager):

    def __init__(self):
        super(DBManager, self).__init__()
        self.model = Manager
        self.params = self.get_editable_fields()
