# -*- coding: utf8 -*-

from core import db


class Manager(db.Model):
    __tablename__ = 'manager'
    __bind_key__ = 'hrms'
    __table_args__ = {"mysql_engine": "InnoDB", "mysql_charset": "utf8"}

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    user_name = db.Column(db.String(32), default='', nullable=False)  # 用户名称
    password = db.Column(db.String(64), default='', nullable=False)  # 密码
    phone = db.Column(db.BigInteger, default=0, nullable=False)  # 电话号码
    email = db.Column(db.String(128), default='', nullable=False)  # 邮箱
    user_status = db.Column(db.SmallInteger, default=1)  # 用户状态1-正常，2-已注销
    is_del = db.Column(db.SmallInteger, default=0)  # 是否删除：0-未删除；1-删除
    create_time = db.Column(db.Integer, default=0)  # 创建时间

