# -*- coding: utf8 -*-
from core import db


class FeConfigure(db.Model):

    __tablename__ = 'fe_configure'
    __bind_key__   = 'hrms'
    __table_args__ = {"mysql_engine":"InnoDB", "mysql_charset":"utf8"}

    id                  = db.Column(db.BigInteger, primary_key=True, nullable=False)
    org_id              = db.Column(db.Integer, default=1)                                    # 公司id
    proj_id             = db.Column(db.Integer, default=0)                                    # 项目id
    page_url              = db.Column(db.String(100, collation='utf8_unicode_ci'), default='')  # 项目所属模块
    gear_id           = db.Column(db.String(100, collation='utf8_unicode_ci'), default='')  # 插件名ID
    props               = db.Column(db.String(500, collation='utf8_unicode_ci'), default='')  # 属性
    props_format               = db.Column(db.String(500, collation='utf8_unicode_ci'), default='')  # 属性

    is_del              = db.Column(db.SmallInteger, default=0)        # 是否删除：0-未删除；1-删除
    create_time         = db.Column(db.Integer)                        # 创建时间
