# -*- encoding: utf8 -*-
from commons.helper.db_manager import DBManager
from hrms.dao.models.proj.proj import Proj


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