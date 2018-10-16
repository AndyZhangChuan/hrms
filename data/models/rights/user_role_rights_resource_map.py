# -*- coding: utf8 -*-

from core import db


class UserRoleRightsResourceMap(db.Model):
    __tablename__ = 'user_role_rights_resource_map'
    __bind_key__ = 'hrms'
    __table_args__ = {"mysql_engine": "InnoDB", "mysql_charset": "utf8"}

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    role_id = db.Column(db.Integer, nullable=False, default=0) # 角色编号
    resource_id = db.Column(db.Integer, nullable=False, default=0) # 资源/权限 编号
    is_del = db.Column(db.SmallInteger, default=0)  # 是否删除：0-未删除；1-删除
    create_time = db.Column(db.Integer, default=0)  # 创建时间

