# -*- encoding: utf8 -*-
from commons.helper.db_manager import DBManager
from data.models.proj.proj_offer import ProjOffer


class ProjOfferManager(DBManager):

    def __init__(self):
        super(DBManager, self).__init__()
        self.model = ProjOffer
        self.params = self.get_editable_fields()
