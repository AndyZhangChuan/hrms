# -*- encoding: utf8 -*-
import datetime

from commons.helper.db_manager import DBManager
from dao.models.proj.proj import Proj


class ProjManager(DBManager):

    def __init__(self):
        super(DBManager, self).__init__()
        self.model = Proj
        self.params = self.get_editable_fields()
        self.params.append('update_time')

    def update_proj_by_id(self, proj_id, params):
        proj = self.get(proj_id)
        if proj is None:
            return None
        return self.update(proj, **params)

    @staticmethod
    def proj_updated(proj_id):
        mgr = ProjManager()
        proj = mgr.get(proj_id)
        if proj is None:
            return None
        now = datetime.datetime.now()
        now = now.strftime("%Y-%m-%d %H:%M:%S")
        mgr.update(proj, update_time=now)

