# -*- encoding: utf8 -*-
from commons.helper.db_manager import DBManager
from core import db
from data.models.proj.proj_offer import ProjOffer


class ProjOfferManager(DBManager):

    def __init__(self):
        super(DBManager, self).__init__()
        self.model = ProjOffer
        self.params = self.get_editable_fields()

    def get_position_options(self, proj_id):
        options = db.session.query(self.model.position).filter(self.model.proj_id == proj_id).all()
        return [item[0] for item in options]