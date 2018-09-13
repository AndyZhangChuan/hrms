# -*- coding: utf8 -*-

from core import db


class ProjPic(db.Model):
    __tablename__ = 'proj_pic'
    __bind_key__ = 'hrms'
    __table_args__ = {"mysql_engine": "InnoDB", "mysql_charset": "utf8"}

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    proj_id = db.Column(db.Integer, default=0)  # 项目编号
    url = db.Column(db.String(256), default='', nullable=False)  # 地址
    is_del = db.Column(db.SmallInteger, default=0)  # 是否删除：0-未删除；1-删除
    create_time = db.Column(db.Integer, default=0)  # 创建时间
