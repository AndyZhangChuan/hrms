# -*- encoding: utf8 -*-
from commons.helper.db_manager import DBManager
from data.models.framework.fe_configure import FeConfigure


class FeConfigureManager(DBManager):

    def __init__(self):
        super(DBManager, self).__init__()
        self.model = FeConfigure
        self.params = self.get_editable_fields()

    def create_or_update(self, proj_id, page_url, gear_id, props, props_format):
        config = self.query_first({'proj_id': proj_id, 'page_url': page_url, 'gear_id': gear_id, 'is_del': 0})
        if config:
            if props:
                config = self.update(config, props=props)
            if props_format:
                config = self.update(config, props_format=props_format)
        else:
            config = self.create(proj_id=proj_id, page_url=page_url, gear_id=gear_id, props=props, props_format=props_format)
        return config