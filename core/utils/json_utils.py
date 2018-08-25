# -*- encoding: utf8 -*-

__author__ = 'zhangchuan'

import re
import json
from datetime import datetime, date

spaces_pattern = re.compile("[\n|\r|\t]")


def to_json(obj):
    if not isinstance(obj, basestring):
        obj = json.dumps(obj, ensure_ascii=False, encoding='utf-8', default=json_default)
    return obj


def to_json_no_tab(data):
    if not isinstance(data, basestring):
        data = to_json(data)
    return trim_tab(data)


def trim_tab(text):
    return re.sub(spaces_pattern, ' ', text)


def json_default(obj):
    if isinstance(obj, datetime):
        return obj.strftime('%Y-%m-%d %H:%M:%S')
    elif isinstance(obj, date):
        return obj.strftime('%Y-%m-%d')
    else:
        return str(obj)
