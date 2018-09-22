# -*- encoding: utf8 -*-

import time
from datetime import datetime, timedelta, date

def dateString2timestampCommon(dateString):
    if '-' in dateString:
        return dateString2timestamp(dateString)
    elif '.' in dateString:
        return timeString2timestampWithFormat('%Y.%m.%d', dateString)
    elif '年' in dateString:
        return timeString2timestampWithFormat('%Y年%m月%d日', dateString)
    else:
        return 0

def dateString2timestamp(dateString):
    """
    年-月-日 => 时间戳
    """
    dateStructure = time.strptime(dateString, "%Y-%m-%d")
    timestamp = int(time.mktime(dateStructure))
    return timestamp


def timeString2timestampWithFormat(format, dateString):
    """
    年-月-日 => 时间戳
    """
    dateStructure = time.strptime(dateString, format)
    timestamp = int(time.mktime(dateStructure))
    return timestamp

def timeString2timestamp(timeString):
    """
    年-月-日 时:分:秒 => 时间戳
    """
    #dateStructure = time.strptime(timeString, "%Y-%m-%d %H:%M:%S")
    timestamp = int(time.mktime(timeString))
    return timestamp

def timestamp2dateString(timestamp):
    """
    时间戳 => 年-月-日
    """
    return time.strftime("%Y-%m-%d", time.localtime(timestamp))

def timestamp2timeString(timestamp):
    """
    时间戳 => 年-月-日 时:分:秒
    """
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timestamp))

def timestamp2timeStringWithFormat(format,timestamp):
    """
    时间戳 => Formatted String
    """
    return time.strftime(format,time.localtime(timestamp))

def todayStartTimestamp():
    """
    今天的第一秒
    """
    return dateString2timestamp(currentDateString())

def todayEndTimestamp():
    """
    今天的最后一秒
    """
    return dateString2timestamp(currentDateString()) + 3600*24

def currentTimestamp():
    """
    当前时间戳
    """
    return int(time.time())

def currentTimeString():
    """
    当前时间：年-月-日 时:分:秒
    """
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))

def currentDateString():
    """
    今天：年-月-日
    """
    return time.strftime("%Y-%m-%d", time.localtime(time.time()))

def currentYear():
    """
    今年
    """
    return time.localtime(time.time()).tm_year

def nextDateString():
    """
    今天的明天：年-月-日
    """
    tomorrow = datetime.now() + timedelta(days=1)
    return tomorrow.strftime("%Y-%m-%d")

def get_yesterday_zero_timestamp():
    from datetime import date, timedelta
    import time
    import sys,datetime
    yesterday_zero = str(date.today() - timedelta(1))+" 00:00:00"
    yesterday_zero_array = time.strptime(yesterday_zero, "%Y-%m-%d %H:%M:%S")
    return int(time.mktime(yesterday_zero_array))


def timeString2timestampV2(timeString):
    """
    年-月-日 时:分:秒 => 时间戳
    """
    dateStructure = time.strptime(timeString, "%Y-%m-%d %H:%M:%S")
    timestamp = int(time.mktime(dateStructure))
    return timestamp

def timeString2timestampV3(timeString):
    """
    年/月/日 时:分:秒 => 时间戳
    """
    dateStructure = time.strptime(timeString, "%Y/%m/%d %H:%M:%S")
    timestamp = int(time.mktime(dateStructure))
    return timestamp

def current_time_string():
    """
    当前时间：时:分:秒
    """
    return time.strftime("%H:%M:%S", time.localtime(time.time()))

def current_datetime_string():
    """
    当前时间：年-月-日 时:分:秒
    """
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))


def yesterday_string():
    """
    明天：年-月-日
    """
    yesterday = datetime.now() - timedelta(days=1)
    return yesterday.strftime("%Y-%m-%d")

def time_delta_string(days):
    """
    返回days天后的日期：年-月-日
    """
    days_later_date = datetime.now() + timedelta(days=days)
    return days_later_date.strftime("%Y-%m-%d")

def get_week_day(weekdelta=0):
    """
    weekdelta: 相对本周相差多少周，如1，则返回下周； -1返回上周的日期
    本周的开始日期(周一)，结束日期(周日)
    """
    weekday = int(time.strftime('%w'))
    today = date.today() + timedelta(days=weekdelta * 7)
    if not weekday:
        return str(today - timedelta(days=6)), str(today)
    else:
        return str(today - timedelta(days=weekday-1)), str(today + timedelta(days=7-weekday))

def get_week_by_date_string(date_string=''):
    '''

    :param date_string: 20160305, 默认值当天
    :return: 当年的第几周 '09'
    '''
    date_str = str(date_string) if date_string else currentDateString().replace('-', '')
    my_date = date(int(date_str[:4]), int(date_str[4:6]), int(date_str[6:8]))
    return my_date.strftime('%W')



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
