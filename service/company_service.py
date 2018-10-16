# -*- encoding: utf8 -*-

from data.manager import CompanyMgr
from commons.utils import page_util


def get_company_list(page):
    order_by_list = [CompanyMgr.model.id.desc()]
    expressions = [CompanyMgr.model.is_del == 0]
    return page_util.get_page_result(CompanyMgr.model, page=page,  expressions=expressions, page_size=10,
                                     filter_func=__company_mapper, order_by_list=order_by_list)


def __company_mapper(company, biz_context):
    '''
    result:[{"company_id": 1, "company_name: "明星人力资源公司", "address": "浦东南路", "company_name": "",
    "crew_num": 100, "description": "", "work_crew_num": 90, "current_month_income": 480001331, "message_count": 6}],
    :param company:
    :return:
    '''

    item = dict()
    item['company_id'] = company.id
    item['address'] = company.address
    item['company_name'] = company.company_name
    item['start_time'] = company.create_time
    item['description'] = company.memo
    # TODO
    item['company_thumbnail'] = company.logo_url
    return item

