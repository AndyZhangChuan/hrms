# -*- coding: utf8 -*-

from core import db


class RichText(db.Model):
    __tablename__ = 'rich_text'
    __bind_key__ = 'hrms'
    __table_args__ = {"mysql_engine": "InnoDB", "mysql_charset": "utf8"}

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    bus_type = db.Column(db.String(128), default='', nullable=False)  # 项目编号
    bus_id = db.Column(db.Integer, default=0)  # 项目编号
    title = db.Column(db.String(128), default='', nullable=False)  # 标题
    subtitle = db.Column(db.String(128), default='', nullable=False)  # 副标题
    text_type = db.Column(db.String(128), default='', nullable=False)  # 文本类型
    sequence = db.Column(db.Integer, default=0)  # 顺序
    rich_text = db.Column(db.Text, default='', nullable=False)  # 富文本
    is_del = db.Column(db.SmallInteger, default=0)  # 是否删除：0-未删除；1-删除
    create_time = db.Column(db.Integer, default=0)  # 创建时间
