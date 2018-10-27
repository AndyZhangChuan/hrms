# -*- encoding: utf8 -*-
from commons.helper.db_manager import DBManager
from data.models.framework.plugin import Plugin


class PluginManager(DBManager):

    def __init__(self):
        super(DBManager, self).__init__()
        self.model = Plugin
        self.params = self.get_editable_fields()

