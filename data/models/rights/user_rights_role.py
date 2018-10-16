# -*- coding: utf8 -*-

from core import db


class UserRightsRole(db.Model):
    __tablename__ = 'user_rights_role'
    __bind_key__ = 'hrms'
    __table_args__ = {"mysql_engine": "InnoDB", "mysql_charset": "utf8"}

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    role_name = db.Column(db.String(64), default='', nullable=False)  # 角色名称
    is_del = db.Column(db.SmallInteger, default=0)  # 是否删除：0-未删除；1-删除
    create_time = db.Column(db.Integer, default=0)  # 创建时间

