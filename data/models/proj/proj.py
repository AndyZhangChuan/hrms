# -*- coding: utf8 -*-

from core import db


class Proj(db.Model):
    __tablename__ = 'proj'
    __bind_key__ = 'hrms'
    __table_args__ = {"mysql_engine": "InnoDB", "mysql_charset": "utf8"}

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    proj_name = db.Column(db.String(64), default='', nullable=False)  # 项目名称
    company_id = db.Column(db.Integer, default=0)  # 所属公司编号
    address = db.Column(db.String(128), default='', nullable=False)  # 地址
    crew_num = db.Column(db.String(128), default='', nullable=False)  # 所需员工数量
    wage_range = db.Column(db.String(128), default='', nullable=False)  # 所需员工数量
    start_time = db.Column(db.Integer, default=0)  # 开始时间
    end_time = db.Column(db.Integer, default=0)  # 结束时间
    tags = db.Column(db.String(), default='', nullable=False)  # 项目描述
    proj_status = db.Column(db.SmallInteger, default=0)  # 项目状态 0-招工(未开始),1-进行中,2-已结束, 3-异常
    category = db.Column(db.SmallInteger, default=0)  # 项目种类(京东/天猫/顺丰等)
    is_del = db.Column(db.SmallInteger, default=0)  # 是否删除：0-未删除；1-删除
    create_time = db.Column(db.Integer, default=0)  # 创建时间
    update_time = db.Column(db.TIMESTAMP, default='')  # 创建时间
