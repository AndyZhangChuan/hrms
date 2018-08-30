# -*- encoding: utf8 -*-
from ...db_manager import DBManager
from hrms.dao.models.hrms.proj.proj_plugin import ProjPlugin


class ProjPluginManager(DBManager):

    def __init__(self):
        super(DBManager, self).__init__()
        self.model = ProjPlugin
        self.params = self.get_editable_fields()
