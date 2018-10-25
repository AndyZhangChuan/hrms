# -*- encoding: utf8 -*-
from commons.helper.db_manager import DBManager
from data.models.framework.rich_text import RichText


class RichTextManager(DBManager):

    def __init__(self):
        super(DBManager, self).__init__()
        self.model = RichText
        self.params = self.get_editable_fields()
        self.parent = 'proj'

    def get_last_sequence_by_type(self, org_id, proj_id, text_type):
        filter_conditions = {'org_id': org_id, 'proj_id': proj_id, 'text_type': text_type, 'is_del': 0}
        last_pic = self.query_first(filter_conditions=filter_conditions, order_list=[self.model.sequence.desc()])
        return last_pic.sequence if last_pic else 1

    def get_richtext_by_type(self, org_id, proj_id, text_type):
        filter_conditions = {'org_id': org_id, 'proj_id': proj_id, 'text_type': text_type, 'is_del': 0}
        return self.query(filter_conditions=filter_conditions, order_list=[self.model.sequence])
