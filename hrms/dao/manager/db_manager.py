# -*- encoding: utf8 -*-
import time

from sqlalchemy import distinct
from sqlalchemy import func

from core import db

UNEDITABLE_FIELDS = ['id', 'is_del', 'create_time', 'update_time']


class DBManager(object):

    def __init__(self):
        self.params = []
        self.model = db.Model

    def _is_field_editable(self, field):
        if field.startswith('_'):
            return False
        if callable(getattr(self.model, field)):
            return False
        if field in UNEDITABLE_FIELDS:
            return False
        return True

    def get_editable_fields(self):
        return filter(lambda field : self._is_field_editable(field), self.model.__dict__.keys())

    def new(self, **kwargs):
        model = self.model()
        for each in self.params:
            if each in kwargs and kwargs[each] != None:
                setattr(model, each, kwargs[each])
        model.is_del = 0
        model.create_time = int(time.time())
        return model

    def create(self, **kwargs):
        model = self.new(**kwargs)
        try:
            db.session.add(model)
            db.session.commit()
        except Exception, e:
            db.session.rollback()
            print e
            model = None
        return model

    def batch_create(self, params_list):
        for params in params_list:
            model = self.new(**params)
            db.session.add(model)

        try:
            db.session.commit()
        except Exception, e:
            db.session.rollback()
            print e
            return False
        return True

    def update(self, model, **kwargs):
        for each in self.params:
            if each in kwargs and kwargs[each] != None:
                setattr(model, each, kwargs[each])
        try:
            db.session.commit()
        except Exception, e:
            db.session.rollback()
            print e
            return None
        return model

    def delete(self, model):
        model.is_del = 1
        try:
            db.session.commit()
        except Exception, e:
            db.session.rollback()
            print e
            return None
        return model

    def restore(self, model):
        model.is_del = 0
        try:
            db.session.commit()
        except Exception, e:
            db.session.rollback()
            print e
            return None
        return model

    def batch_delete(self, models):
        for model in models:
            model.is_del = 1
        try:
            db.session.commit()
        except Exception, e:
            db.session.rollback()
            print e
            return None
        return models

    def batch_update(self, models, **kwargs):
        for model in models:
            for each in self.params:
                if each in kwargs and kwargs[each] is not None:
                    setattr(model, each, kwargs[each])
        try:
            db.session.commit()
        except Exception, e:
            db.session.rollback()
            print e
            return None
        return models

    def batch_update_multi(self, models, params_list):
        assert len(models) == len(params_list)
        for i in range(len(models)):
            model = models[i]
            params = params_list[i]
            for each in self.params:
                if each in params and params[each] is not None:
                    setattr(model, each, params[each])
        try:
            db.session.commit()
        except Exception, e:
            db.session.rollback()
            print e
            return None
        return models

    def get(self, id):
        return self.model.query.get(id)

    def query_common(self, filter_conditions={}, order_list=[], limit=0, offset=0, expressions=[], entities=[], group_by_list=[]):
        ret = self.model.query
        if filter_conditions and len(filter_conditions) > 0:
            ret = ret.filter_by(**filter_conditions)
        if expressions and len(expressions) > 0:
            ret = ret.filter(*expressions)
        if entities and len(entities) > 0:
            ret = ret.with_entities(*entities)
        if order_list and len(order_list) > 0:
            ret = ret.order_by(*order_list)
        if group_by_list and len(group_by_list) > 0:
            ret = ret.group_by(*group_by_list)
        if limit:
            ret = ret.limit(limit)
        if offset:
            ret = ret.offset(offset)
        return ret

    def query(self, filter_conditions={}, order_list=[], limit=0, offset=0, expressions=[], entities=[], group_by_list=[]):
        return self.query_common(filter_conditions, order_list, limit, offset, expressions, entities, group_by_list).all()

    def query_first(self, filter_conditions={}, order_list=[], expressions=[], entities=[], group_by_list=[]):
        return self.query_common(filter_conditions, order_list, expressions=expressions, entities=entities, group_by_list=group_by_list).first()

    def count(self, filter_conditions={}, expressions=[], field='id', use_distinct=False):
        assert hasattr(self.model, field)
        entities = func.count(getattr(self.model, field))
        if use_distinct:
            entities = distinct(entities)
        ret = db.session.query(entities)
        if filter_conditions and len(filter_conditions) > 0:
            ret = ret.filter_by(**filter_conditions)
        if expressions and len(expressions) > 0:
            ret = ret.filter(*expressions)
        return ret.scalar()

    def sum(self, field, filter_conditions={}, expressions=[]):
        assert hasattr(self.model, field)
        ret = db.session.query(func.sum(getattr(self.model, field)))
        if filter_conditions and len(filter_conditions) > 0:
            ret = ret.filter_by(**filter_conditions)
        if expressions and len(expressions) > 0:
            ret = ret.filter(*expressions)
        return ret.scalar()
