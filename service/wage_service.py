# coding=utf-8
import json

from core.framework.plugin import execute_proj_plugin
from dao.manager import WageMgr, WageRawDataMgr
from service.constant import proj_nodes


def get_input_format(proj_id):
    data = {}
    execute_result = execute_proj_plugin(proj_id, proj_nodes.WAGE_DATA_INPUT, {}, data)
    if execute_result['status'] != 'ok':
        return execute_result['data']
    else:
        return data


def create_wage_raw_data(proj_id, lines):
    execute_result = execute_proj_plugin(proj_id, proj_nodes.WAGE_DATA_ADD, {}, {'proj_id': proj_id, 'lines': lines, 'errors': []})
    data = execute_result['data']
    for record in data['wage_raw_datas']:
        record['meta'] = json.dumps(record['meta'])
        WageRawDataMgr.create_override_if_exist(record)
    for record in data['wage']:
        record['meta'] = json.dumps(record['meta'])
        WageMgr.create_override_if_exist(record)
    return execute_result


def get_wage_records(proj_id, page, filters):
    filter_condition = {'is_del': 0}
    expressions = []
    if 0 < filters['startTime'] < filters['endTime']:
        expressions = [WageMgr.model.wage_time > filters['startTime'], WageMgr.model.wage_time < filters['endTime']]
    if 'crew_id' in filters and filters['crew_id']:
        expressions.append(WageMgr.model.crew_id == filters['crew_id'])
    count = WageMgr.count(expressions=expressions, filter_conditions=filter_condition)
    if page != 0:
        records = WageMgr.query(expressions=expressions, filter_conditions=filter_condition, limit=10,
                                offset=(page - 1) * 10, order_list=[WageMgr.model.wage_time.desc()])
    else:
        if count > 5000:  # 数据量过大保护
            records = WageMgr.query(expressions=expressions, filter_conditions=filter_condition, limit=5000,
                                    order_list=[WageMgr.model.wage_time.desc()])
        else:
            records = WageMgr.query(expressions=expressions, filter_conditions=filter_condition)
    data = {'proj_id': proj_id, 'count': count, 'records': records}
    execute_result = execute_proj_plugin(proj_id, proj_nodes.WAGE_DATA_OUTPUT, {}, data)
    data = execute_result['data']
    data['result'] = json.dumps(data['result'])
    data['records'] = None
    return execute_result