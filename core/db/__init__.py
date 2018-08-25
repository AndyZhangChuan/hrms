# -*- encoding: utf8 -*-

from functools import wraps
import uuid
from .router import read_or_write

__author__ = 'zhangchuan'


def force_read_slave(bind_key, db_name):
    """
    强制读取某个从库
    :param bind_key:
    :param db_name:
    :return:
    """
    def read_slave(fn):
        @wraps(fn)
        def decorated_function(*args, **kwargs):
            # 默认走主库，若有配置此拦截器，强制走从库
            old_rw = ''
            old_uuid = ''
            old_force_db_name = ''
            old_bind_key = ''
            old_read_type = ''

            if read_or_write.__dict__.has_key('force_db_name'):
                old_force_db_name = read_or_write.__dict__['force_db_name']
            if read_or_write.__dict__.has_key('bind_key'):
                old_bind_key = read_or_write.__dict__['bind_key']
            if read_or_write.__dict__.has_key('read_or_write'):
                old_rw = read_or_write.__dict__['read_or_write']
            if read_or_write.__dict__.has_key('read_type'):
                old_read_type = read_or_write.__dict__['read_type']
            if read_or_write.__dict__.has_key('uuid'):
                old_uuid = read_or_write.__dict__['uuid']

            read_or_write.__dict__['read_type'] = 'force_read'
            read_or_write.__dict__['read_or_write'] = 'read'
            read_or_write.__dict__['force_db_name'] = db_name
            read_or_write.__dict__['uuid'] = str(uuid.uuid1()).replace('-', '')
            read_or_write.__dict__['bind_key'] = bind_key
            try:
                return fn(*args, **kwargs)
            finally:
                # 清空线程变量
                read_or_write.__dict__['read_or_write'] = old_rw
                read_or_write.__dict__['force_db_name'] = old_force_db_name
                read_or_write.__dict__['uuid'] = old_uuid
                read_or_write.__dict__['bind_key'] = old_bind_key
                read_or_write.__dict__['read_type'] = old_read_type

        return decorated_function

    return read_slave


def read(db_name=None):
    """
    use @read(),can satisfy all you require,include diff logic db to read.
    """

    def read_slave(fn):
        @wraps(fn)
        def decorated_function(*args, **kwargs):
            # 默认走主库，若有配置此拦截器，强制走从库
            old_rw = ''
            old_db_name = ''
            old_uuid = ''

            if read_or_write.__dict__.has_key('db_name'):
                old_db_name = read_or_write.__dict__['db_name']

            if read_or_write.__dict__.has_key('read_or_write'):
                old_rw = read_or_write.__dict__['read_or_write']
            read_or_write.__dict__['read_or_write'] = 'read'
            if read_or_write.__dict__.has_key('uuid'):
                old_uuid = read_or_write.__dict__['uuid']
            read_or_write.__dict__['uuid'] = str(uuid.uuid1()).replace('-', '')
            read_or_write.__dict__['db_name'] = db_name
            try:
                return fn(*args, **kwargs)
            finally:
                # 清空线程变量
                read_or_write.__dict__['read_or_write'] = old_rw
                read_or_write.__dict__['db_name'] = old_db_name
                read_or_write.__dict__['uuid'] = old_uuid

        return decorated_function

    return read_slave

