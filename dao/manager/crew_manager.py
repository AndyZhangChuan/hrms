# -*- encoding: utf8 -*-
from sqlalchemy import or_

from commons.helper.db_manager import DBManager
from dao.models.crew import Crew


class CrewManager(DBManager):

    def __init__(self):
        super(DBManager, self).__init__()
        self.model = Crew
        self.params = self.get_editable_fields()

    def create_override_if_exist(self, record):
        history_record = self.query_first({'is_del': 0}, expressions=[or_(self.model.id_card_num == record['id_card_num'], self.model.id == record['crew_id'])])
        if history_record:
            return self.update(history_record, **record)
        else:
            return self.create(**record)

    def get_crew_obj_by_id(self, id):
        return self.query_first({'id': id})

    def get_crew_id_by_account(self, account):
        crew = self.query_first({'crew_account': account, 'is_del': 0})
        return crew.id if crew else None

    def get_crew_base_info_by_id(self, id):
        crew = self.query_first({'id': id})
        return {'crew_name': crew.crew_name, 'crew_account': crew.crew_account} if crew else None

    def append_crew_base_info_by_account(self, record, account):
        return

    @staticmethod
    def translate_source(source):
        source_dict = {
            0: '网招报名',
            1: '供应商',
            2: '员工推荐',
        }
        return source_dict[int(source)]

    @staticmethod
    def translate_work_status(status):
        status_dict = {
            0: '空闲',
            1: '工作中',
        }
        return status_dict[int(status)]