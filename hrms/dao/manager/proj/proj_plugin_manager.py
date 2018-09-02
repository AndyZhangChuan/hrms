# -*- encoding: utf8 -*-
from commons.helper.db_manager import DBManager
from hrms.dao.models.proj.proj_plugin import ProjPlugin


class ProjPluginManager(DBManager):

    def __init__(self):
        super(DBManager, self).__init__()
        self.model = ProjPlugin
        self.params = self.get_editable_fields()
