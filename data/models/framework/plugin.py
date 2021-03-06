# -*- coding: utf8 -*-
from core import db


class Plugin(db.Model):

    __tablename__ = 'plugin'
    __bind_key__   = 'hrms'
    __table_args__ = {"mysql_engine":"InnoDB", "mysql_charset":"utf8"}

    id                  = db.Column(db.BigInteger, primary_key=True, nullable=False)
    bus_type            = db.Column(db.String(128), default='', nullable=False)  # 项目编号
    bus_id              = db.Column(db.Integer, default=0)  # 项目编号
    category            = db.Column(db.String(100, collation='utf8_unicode_ci'), default='')  # 项目所属模块
    plugin_id           = db.Column(db.String(100, collation='utf8_unicode_ci'), default='')  # 插件名ID
    plugin_name         = db.Column(db.String(100, collation='utf8_unicode_ci'), default='')  # 插件名
    props               = db.Column(db.String(500, collation='utf8_unicode_ci'), default='')  # 属性

    is_del              = db.Column(db.SmallInteger, default=0)        # 是否删除：0-未删除；1-删除
    create_time         = db.Column(db.Integer)                        # 创建时间
