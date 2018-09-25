# -*- encoding: utf8 -*-
from commons.helper.db_manager import DBManager
from dao.models.crew import Crew


class CrewManager(DBManager):

    def __init__(self):
        super(DBManager, self).__init__()
        self.model = Crew
        self.params = self.get_editable_fields()

    def create_override_if_exist(self, record):
        history_record = self.query_first({'id_card_num': record['id_card_num'], 'is_del': 0})
        if history_record:
            return self.update(history_record, **record)
        else:
            return self.create(**record)

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