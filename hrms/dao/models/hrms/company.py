# -*- coding: utf8 -*-

from core import db


class Company(db.Model):
    __tablename__ = 'company'
    __bind_key__ = 'hrms'
    __table_args__ = {"mysql_engine": "InnoDB", "mysql_charset": "utf8"}

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    company_name = db.Column(db.String(128), default='', nullable=False)  # 公司名称
    address = db.Column(db.String(128), default='', nullable=False)  # 地址
    memo = db.Column(db.String(128), default='', nullable=False)  # 备注
    is_del = db.Column(db.SmallInteger, default=0)  # 是否删除：0-未删除；1-删除
    create_time = db.Column(db.Integer, default=0)  # 创建时间
