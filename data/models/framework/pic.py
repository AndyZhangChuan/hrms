# -*- coding: utf8 -*-

from core import db


class Pic(db.Model):
    __tablename__ = 'pic'
    __bind_key__ = 'hrms'
    __table_args__ = {"mysql_engine": "InnoDB", "mysql_charset": "utf8"}

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    bus_type = db.Column(db.String(128), default='', nullable=False)  # 项目编号
    bus_id = db.Column(db.Integer, default=0)  # 项目编号
    img_type = db.Column(db.String(128), default='', nullable=False)  # 图片类型
    sequence = db.Column(db.Integer, default=0)  # 顺序
    url = db.Column(db.String(256), default='', nullable=False)  # 地址
    is_del = db.Column(db.SmallInteger, default=0)  # 是否删除：0-未删除；1-删除
    create_time = db.Column(db.Integer, default=0)  # 创建时间
