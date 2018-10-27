# -*- coding: utf8 -*-
from core import db


class ProjOffer(db.Model):

    __tablename__ = 'proj_offer'
    __bind_key__   = 'hrms'
    __table_args__ = {"mysql_engine":"InnoDB", "mysql_charset":"utf8"}

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    proj_id = db.Column(db.Integer, default=0)  # 项目编号
    offer_type = db.Column(db.Integer, default=0)  # 0-员工到手 1-供应商收入 2-给渠道商收入
    position = db.Column(db.String(128), default='', nullable=False)  # 岗位
    standard_value = db.Column(db.DECIMAL(10,4), default='0.0000', nullable=False)  # 岗位
    start_time = db.Column(db.Integer, default=0)  # 生效时间
    end_time = db.Column(db.Integer, default=0)  # 失效时间
    is_del = db.Column(db.SmallInteger, default=0)  # 是否删除：0-未删除；1-删除
    create_time = db.Column(db.Integer, default=0)  # 创建时间


