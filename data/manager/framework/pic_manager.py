# -*- encoding: utf8 -*-
from commons.helper.db_manager import DBManager
from data.models.framework.pic import Pic


class PicManager(DBManager):

    def __init__(self):
        super(DBManager, self).__init__()
        self.model = Pic
        self.params = self.get_editable_fields()
        self.parent = 'proj'

    def clear_pic_list(self, org_id, proj_id, img_type):
        filter_conditions = {'org_id': org_id, 'proj_id': proj_id, 'img_type': img_type, 'is_del': 0}
        pic_list = self.query(filter_conditions=filter_conditions)
        self.batch_delete(pic_list)

    def get_last_sequence_by_type(self, org_id, proj_id, img_type):
        filter_conditions = {'org_id': org_id, 'proj_id': proj_id, 'img_type': img_type, 'is_del': 0}
        last_pic = self.query_first(filter_conditions=filter_conditions, order_list=[self.model.sequence.desc()])
        return last_pic.sequence

    def get_img_by_type(self, org_id, proj_id, img_type):
        filter_conditions = {'org_id': org_id, 'proj_id': proj_id, 'img_type': img_type, 'is_del': 0}
        return self.query(filter_conditions=filter_conditions, order_list=[self.model.sequence])
