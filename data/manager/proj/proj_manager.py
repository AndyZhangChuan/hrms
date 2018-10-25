# -*- encoding: utf8 -*-
import datetime

from commons.helper.db_manager import DBManager
from data.models.proj.proj import Proj


class ProjManager(DBManager):

    def __init__(self):
        super(DBManager, self).__init__()
        self.model = Proj
        self.params = self.get_editable_fields()
        self.gen_params = ['logo_url', 'intro_list_pics']
