# -*- encoding: utf8 -*-
from commons.helper.db_manager import DBManager
from dao.models.proj import ProjPlugin


class ProjPluginManager(DBManager):

    def __init__(self):
        super(DBManager, self).__init__()
        self.model = ProjPlugin
        self.params = self.get_editable_fields()
