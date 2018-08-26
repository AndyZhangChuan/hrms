# -*- encoding: utf8 -*-
from ...db_manager import DBManager
from hrms.dao.models.hrms.proj.proj_op_log import ProjOpLog


class ProjOpLogManager(DBManager):

    def __init__(self):
        super(DBManager, self).__init__()
        self.model = ProjOpLog
        self.params = self.get_editable_fields()
