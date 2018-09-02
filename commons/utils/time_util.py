# -*- encoding: utf8 -*-
import time


def format_time(timestamp=None):
    """
    将时间戳格式化为可读形式
    timestamp: 时间戳，若不传则为当前时间
    :return: 比如'2017-08-08 00:00:00'
    """
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp))

def current_timestamp():
    return int(time.time())

def date_to_timestamp(date):
    return int(time.mktime(date.timetuple()))
