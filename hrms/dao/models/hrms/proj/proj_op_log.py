# -*- coding: utf8 -*-

from core import db


class ProjOpLog(db.Model):
    __tablename__ = 'proj_op_log'
    __bind_key__ = 'hrms'
    __table_args__ = {"mysql_engine": "InnoDB", "mysql_charset": "utf8"}

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    operator_id = db.Column(db.Integer, default=0)  # 操作人员编号
    proj_id = db.Column(db.Integer, default=0)  # 项目编号
    op_type = db.Column(db.SmallInteger, default=0)  # 项目编号
    from_status = db.Column(db.SmallInteger, default=0)  # 更改前状态
    to_status = db.Column(db.SmallInteger, default=0)  # 更改后状态
    memo = db.Column(db.String(256), default='', nullable=False)  # 操作类型：1-创建，2-更改，3-删除，4，状态变更
    is_del = db.Column(db.SmallInteger, default=0)  # 是否删除：0-未删除；1-删除
    create_time = db.Column(db.Integer, default=0)  # 创建时间
