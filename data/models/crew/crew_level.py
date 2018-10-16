# -*- coding: utf8 -*-
from core import db


class CrewLevel(db.Model):

    __tablename__ = 'crew_level'
    __bind_key__   = 'hrms'
    __table_args__ = {"mysql_engine":"InnoDB", "mysql_charset":"utf8"}

    id = db.Column(db.BigInteger, primary_key=True, nullable=False, autoincrement=True)
    crew_id = db.Column(db.BigInteger, default=0, nullable=False)  # 员工帐号
    level = db.Column(db.Integer, default=0)  # 员工手机号
    level_name = db.Column(db.String(128), default='', nullable=False)  # 身份证号
    accumulate_work_days = db.Column(db.Integer, default=0)  # 累计工作天数
    meta = db.Column(db.String(512, collation='utf8_unicode_ci'), default='')  # 其他信息
    is_del = db.Column(db.SmallInteger, default=0) #是否删除：0-未删除；1-删除
    create_time = db.Column(db.Integer, default=0) #创建时间


