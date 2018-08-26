# -*- encoding: utf8 -*-
from ..db_manager import DBManager
from hrms.dao.models.hrms.company import Company


class CompanyManager(DBManager):

    def __init__(self):
        super(DBManager, self).__init__()
        self.model = Company
        self.params = self.get_editable_fields()

    def get_companies_by_ids(self, company_ids):
        expressions = [Company.id.in_(company_ids)]
        return self.query(expressions=expressions)