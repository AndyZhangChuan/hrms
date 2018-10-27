# -*- coding: utf8 -*-
from core import db


class OrgProjMap(db.Model):

    __tablename__ = 'org_proj_map'
    __bind_key__   = 'hrms'
    __table_args__ = {"mysql_engine":"InnoDB", "mysql_charset":"utf8"}

    id                  = db.Column(db.BigInteger, primary_key=True, nullable=False)
    org_id          = db.Column(db.Integer, nullable=False, default=1)
    proj_id             = db.Column(db.Integer, nullable=False, default=0)

    is_del              = db.Column(db.SmallInteger, default=0)        # 是否删除：0-未删除；1-删除
    create_time         = db.Column(db.Integer)                        # 创建时间
