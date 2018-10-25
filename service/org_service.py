# -*- encoding: utf8 -*-

from data.manager import OrgMgr
from commons.utils import page_util, to_dict


def get_org_list():
    return to_dict(OrgMgr.query({'is_del': 0}))


def __org_mapper(org, biz_context):
    '''
    result:[{"org_id": 1, "org_name: "明星人力资源公司", "address": "浦东南路", "org_name": "",
    "crew_num": 100, "description": "", "work_crew_num": 90, "current_month_income": 480001331, "message_count": 6}],
    :param org:
    :return:
    '''

    item = dict()
    item['org_id'] = org.id
    item['org_name'] = org.org_name
    return item

