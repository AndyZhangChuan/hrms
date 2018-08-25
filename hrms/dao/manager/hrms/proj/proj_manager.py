# -*- encoding: utf8 -*-
from ...db_manager import DBManager
from hrms.dao.models.hrms.proj import Proj


class ProjManager(DBManager):

    def __init__(self):
        super(DBManager, self).__init__()
        self.model = Proj
        self.params = self.get_editable_fields()
