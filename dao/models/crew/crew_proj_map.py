# -*- coding: utf8 -*-
from core import db


class CrewProjMap(db.Model):

    __tablename__ = 'crew_proj_map'
    __bind_key__   = 'hrms'
    __table_args__ = {"mysql_engine":"InnoDB", "mysql_charset":"utf8"}

    id = db.Column(db.BigInteger, primary_key=True, nullable=False, autoincrement=True)
    crew_id = db.Column(db.BigInteger, default=0, nullable=False)  # 员工帐号
    proj_id = db.Column(db.Integer, default=0)  # 项目编号
    start_time = db.Column(db.Integer, default=0)  # 开工时间
    entry_status = db.Column(db.SmallInteger, default=0)  #审核状态：0-报名，1-审核通过/已入职，2-审核驳回
    is_del = db.Column(db.SmallInteger, default=0) #是否删除：0-未删除；1-删除
    create_time = db.Column(db.Integer, default=0) #创建时间


