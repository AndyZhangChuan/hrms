# -*- encoding: utf8 -*-
from commons.helper.db_manager import DBManager
from data.models.framework.dao_relation_map import DaoRelationMap


class DaoRelationMapManager(DBManager):

    def __init__(self):
        super(DBManager, self).__init__()
        self.model = DaoRelationMap
        self.params = self.get_editable_fields()
