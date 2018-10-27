# -*- encoding: utf8 -*-
from commons.helper.db_manager import DBManager
from data.models.crew.crew_level import CrewLevel


class CrewLevelManager(DBManager):

    def __init__(self):
        super(DBManager, self).__init__()
        self.model = CrewLevel
        self.params = self.get_editable_fields()
        self.parent = 'crew'
