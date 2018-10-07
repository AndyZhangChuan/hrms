# -*- coding: utf8 -*-
from core import db


class Crew(db.Model):

    __tablename__ = 'crew'
    __bind_key__   = 'hrms'
    __table_args__ = {"mysql_engine":"InnoDB", "mysql_charset":"utf8"}

    id = db.Column(db.BigInteger, primary_key=True, nullable=False, autoincrement=True)
    crew_account = db.Column(db.String(128), default='', nullable=False)  # 员工帐号
    crew_name = db.Column(db.String(128), default='', nullable=False)  # 员工姓名
    phone = db.Column(db.Integer, default=0)  # 员工手机号
    id_card_num = db.Column(db.String(128), default='', nullable=False)  # 身份证号
    supplier_name = db.Column(db.String(128), default='', nullable=False)  # 供应商
    source = db.Column(db.SmallInteger, default=0) #是否删除：0-网招；1-供应商导入 2-员工推荐 3-其他

    work_status = db.Column(db.SmallInteger, default=0) #工作状态 0-空闲 1-已入职 -1-黑名单
    meta = db.Column(db.String(512, collation='utf8_unicode_ci'), default='')  # 收入备注
    is_del = db.Column(db.SmallInteger, default=0) #是否删除：0-未删除；1-删除
    create_time = db.Column(db.Integer, default=0) #创建时间


