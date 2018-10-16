# -*- coding: utf8 -*-

from core import db


class UserRightsResource(db.Model):
    __tablename__ = 'user_rights_resource'
    __bind_key__ = 'hrms'
    __table_args__ = {"mysql_engine": "InnoDB", "mysql_charset": "utf8"}

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    resource_name = db.Column(db.String(64), default='', nullable=False)  # 资源/权限名称
    short_name = db.Column(db.String(128), default='', nullable=False)  # 英文简称（必填），程序控制唯
    value = db.Column(db.String(256), default='', nullable=False)  # 资源值/url
    resource_type = db.Column(db.SmallInteger, default=1)  # 资源类型： 1-资源，2-资源组
    parent_id = db.Column(db.Integer, default=0, nullable=False) # 0-为顶级资源
    rank = db.Column(db.Integer, default=1, nullable=False) # 排序
    is_del = db.Column(db.SmallInteger, default=0)  # 是否删除：0-未删除；1-删除
    create_time = db.Column(db.Integer, default=0)  # 创建时间

