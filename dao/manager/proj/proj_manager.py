# -*- encoding: utf8 -*-
from commons.helper.db_manager import DBManager
from dao.models.proj.proj import Proj


class ProjManager(DBManager):

    def __init__(self):
        super(DBManager, self).__init__()
        self.model = Proj
        self.params = self.get_editable_fields()

    def update_proj_by_id(self, proj_id, params):
        proj = self.get(proj_id)
        if proj is None:
            return None
        return self.update(proj, **params)

    def get_proj_by_ids(self, proj_ids):
        expressions = [self.model.id.in_(proj_ids)]
        return self.query(expressions=expressions)
