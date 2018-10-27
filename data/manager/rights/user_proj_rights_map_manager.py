# -*- encoding: utf8 -*-
from commons.helper.db_manager import DBManager
from data.models.rights.user_proj_rights_map import UserProjRightsMap


class UserProjRightsMapManager(DBManager):

    def __init__(self):
        super(DBManager, self).__init__()
        self.model = UserProjRightsMap
        self.params = self.get_editable_fields()

    def delete_rights_by_manager_id(self, manager_id):
        filter_conditions = {'manager_id': manager_id, 'is_del': 0}
        models = self.query(filter_conditions=filter_conditions)
        self.batch_delete(models)

    def allocate_rights_by_company_ids(self, manager_id, company_ids):
        company_ids = list(set(company_ids))
        param_list = [{'manager_id': manager_id, 'company_id': company_id} for company_id in company_ids]
        return self.batch_create(param_list)

    def allocate_rights_by_company_proj_list(self, manager_id, company_proj_map):
        param_list = [{'manager_id': manager_id, 'company_id': item['company_id'], 'proj_id': item['proj_id']} for item
                      in company_proj_map]
        return self.batch_create(param_list)

    def get_rights_by_manager_id(self, manager_id):
        filter_conditions = {'manager_id': manager_id, 'is_del': 0}
        return self.query(filter_conditions=filter_conditions)