# -*- coding: utf8 -*-
from core import db


class DaoRelationMap(db.Model):

    __tablename__ = 'dao_relation_map'
    __bind_key__   = 'hrms'
    __table_args__ = {"mysql_engine":"InnoDB", "mysql_charset":"utf8"}

    id                  = db.Column(db.BigInteger, primary_key=True, nullable=False)
    dao                 = db.Column(db.String(100, collation='utf8_unicode_ci'), default='')
    plugin_id           = db.Column(db.String(100, collation='utf8_unicode_ci'), default='')
    attr_name           = db.Column(db.String(100, collation='utf8_unicode_ci'), default='')
    input_args          = db.Column(db.String(200, collation='utf8_unicode_ci'), default='')
    type                = db.Column(db.String(100, collation='utf8_unicode_ci'), default='')
    comment             = db.Column(db.String(500, collation='utf8_unicode_ci'), default='')

    is_del              = db.Column(db.SmallInteger, default=0)        # 是否删除：0-未删除；1-删除
    create_time         = db.Column(db.Integer)                        # 创建时间
