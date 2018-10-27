# -*- encoding: utf8 -*-
from commons.helper.db_manager import DBManager
from data.models.framework.org_proj_map import OrgProjMap


class OrgProjMapManager(DBManager):

    def __init__(self):
        super(DBManager, self).__init__()
        self.model = OrgProjMap
        self.params = self.get_editable_fields()

    def register_proj(self, org_id):
        item = self.create(org_id=org_id)
        self.update(item, proj_id=item.id)
        return item.id
