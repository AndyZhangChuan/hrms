# -*- encoding: utf8 -*-
from commons.helper.db_manager import DBManager
from data.models.crew.crew_proj_map import CrewProjMap


class CrewProjMapManager(DBManager):

    def __init__(self):
        super(DBManager, self).__init__()
        self.model = CrewProjMap
        self.params = self.get_editable_fields()
        self.is_map = True

    @staticmethod
    def translate_entry_status(status):
        status_dict = {
            0: '待审核',
            1: '审核通过',
            2: '审核失败',
        }
        return status_dict[int(status)]