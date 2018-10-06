# -*- encoding: utf8 -*-
from commons.helper.db_manager import DBManager
from dao.manager.proj import ProjManager
from dao.models.proj import ProjRichText


class ProjRichTextManager(DBManager):

    def __init__(self):
        super(DBManager, self).__init__()
        self.model = ProjRichText
        self.params = self.get_editable_fields()

    def get_last_sequence_by_type(self, proj_id, text_type):
        filter_conditions = {'proj_id': proj_id, 'text_type': text_type, 'is_del': 0}
        last_pic = self.query_first(filter_conditions=filter_conditions, order_list=[self.model.sequence.desc()])
        return last_pic.sequence if last_pic else 1

    def get_richtext_by_type(self, proj_id, text_type):
        filter_conditions = {'proj_id': proj_id, 'text_type': text_type, 'is_del': 0}
        return self.query(filter_conditions=filter_conditions, order_list=[self.model.sequence])

    def update(self, model, **kwargs):
        ProjManager.proj_updated(model.proj_id)
        return super(ProjRichTextManager, self).update(model, **kwargs)

    def create(self, **kwargs):
        ProjManager.proj_updated(kwargs['proj_id'])
        return super(ProjRichTextManager, self).create(**kwargs)

    def delete(self, model, **kwargs):
        ProjManager.proj_updated(model.proj_id)
        return super(ProjRichTextManager, self).delete(model)
