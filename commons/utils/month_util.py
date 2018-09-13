# -*- encoding: utf8 -*-

import time, datetime


def get_next_month(m=''):

    if m:
        x = m.split('-')
        cul_date = datetime.date(int(x[0]), int(x[1]), 1)
    else:
        cul_date = datetime.date.today()

    next_month = (cul_date.month + 1) % 12 if cul_date.month != 11 else 12
    next_year = cul_date.year
    if cul_date.month == 12:
        next_year += 1
    next_month_time = datetime.date(next_year, next_month, 1)
    return next_month_time


def get_month_first_date(m=''):
    if m:
        x = m.split('-')
        cul_date = datetime.date(int(x[0]), int(x[1]), 1)
    else:
        cul_date = datetime.date.today()
    return get_month_period(cul_date)[0]


def get_last_month(m=''):

    if m:
        x = m.split('-')
        cul_date = datetime.date(int(x[0]), int(x[1]), 1)
    else:
        cul_date = datetime.date.today()

    last_month = cul_date.month - 1 if cul_date.month > 1 else 12
    last_year = cul_date.year
    if last_month == 12:
        last_year -= 1
    last_month_time = datetime.date(last_year, last_month, 1)
    return last_month_time


def get_cur_month_period(m=None):
    """
    获取几月份的时间区间
    :param m:
    :return:  timestamp
    """

    if m:
        x = m.split('-')
        cul_date = datetime.date(int(x[0]), int(x[1]), 1)
    else:
        cul_date = datetime.date.today()

    month_start_time, month_end_time = get_month_period(cul_date)

    start_timestamp = int(time.mktime(month_start_time.timetuple()))
    end_timestamp = int(time.mktime(month_end_time.timetuple()))

    return start_timestamp, end_timestamp


def get_last_year_today_date(m=None):
    """
    获取指定日期日期的上一年
    :param m:
    :return:
    """
    if m:
        x = m.split('-')
        return datetime.date(int(x[0]) - 1, int(x[1]), 1)

    cul_date = datetime.date.today()
    return datetime.date(cul_date.year, cul_date.month, cul_date.day)


def get_month_period(cul_date):
    """
    获取月份区间,
    :param cul_date:
    :return:  datetime.date
    """
    month_start_time = datetime.date(cul_date.year, cul_date.month, 1)
    next_month = (cul_date.month + 1) % 12 if cul_date.month != 11 else 12
    next_year = cul_date.year
    if cul_date.month == 12:
        next_year += 1
    month_end_time = datetime.date(next_year, next_month, 1)
    return month_start_time, month_end_time


def get_last_timestamp(cur_timestamp):
    """
    获取上个月开始时间戳
    :param cur_timestamp:
    :return:
    """
    m = time.strftime("%Y-%m", time.localtime(cur_timestamp))
    x = m.split('-')
    cul_date = datetime.date(int(x[0]), int(x[1]), 1)
    last_month = (cul_date.month - 1) if cul_date.month != 1 else 12
    last_year = cul_date.year
    if cul_date.month == 1:
        last_year -= 1
    last_month_time = datetime.date(last_year, last_month, 1)
    last_timestamp = int(time.mktime(last_month_time.timetuple()))

    return last_timestamp
