# -*- coding: utf8 -*-

from core import db


class WageRawData(db.Model):
    __tablename__ = 'wage_raw_data'
    __bind_key__ = 'hrms'
    __table_args__ = {"mysql_engine": "InnoDB", "mysql_charset": "utf8"}

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    proj_id = db.Column(db.Integer, default=0)  # 项目编号
    crew_id = db.Column(db.Integer, default=0)  # 员工编号
    bill_id = db.Column(db.String(128), default='', nullable=False)  # 业务id
    position = db.Column(db.String(128), default='', nullable=False)  # 岗位
    work_hours = db.Column(db.DECIMAL(precision=10, scale=2), nullable=False, default=0.00)  # 工作时长
    work_amount = db.Column(db.DECIMAL(precision=10, scale=2), nullable=False, default=0.00)  # 工作量
    wage_time = db.Column(db.Integer, default=0)  # 生产时间
    meta = db.Column(db.String(512), default='', nullable=False)  # 其他信息
    is_del = db.Column(db.SmallInteger, default=0)  # 是否删除：0-未删除；1-删除
    create_time = db.Column(db.Integer, default=0)  # 创建时间
