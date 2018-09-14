# -*- encoding: utf8 -*-
from commons.helper.db_manager import DBManager
from dao.models.proj import ProjPic


class ProjPicManager(DBManager):

    def __init__(self):
        super(DBManager, self).__init__()
        self.model = ProjPic
        self.params = self.get_editable_fields()

    def clear_pic_list(self, proj_id):
        filter_conditions = {'proj_id': proj_id}
        pic_list = self.query(filter_conditions=filter_conditions)
        self.batch_delete(pic_list)