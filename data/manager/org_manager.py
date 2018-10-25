# -*- encoding: utf8 -*-
from commons.helper.db_manager import DBManager
from data.models.org import Org


class OrgManager(DBManager):

    def __init__(self):
        super(DBManager, self).__init__()
        self.model = Org
        self.params = self.get_editable_fields()

    def get_companies_by_ids(self, org_ids):
        expressions = [Org.id.in_(org_ids)]
        return self.query(expressions=expressions)