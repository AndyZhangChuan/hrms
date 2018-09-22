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
    execute_result = execute_proj_plugin(proj_id, proj_nodes.WAGE_DATA_ADD, {}, {'proj_id': proj_id, 'lines': lines})
    data = execute_result['data']
    for record in data['wage_raw_datas']:
        record['meta'] = json.dumps(record['meta'])
        WageRawDataMgr.create_override_if_exist(record)
    for record in data['wage']:
        record['meta'] = json.dumps(record['meta'])
        WageMgr.create_override_if_exist(record)

    if execute_result['status'] != 'ok':
        return execute_result['data']
    else:
        return data


def get_wage_records(proj_id, page, filters):
    data = {'proj_id': proj_id, 'page': page, 'filters': filters}
    execute_result = execute_proj_plugin(proj_id, proj_nodes.WAGE_DATA_OUTPUT, {}, data)
    data = execute_result['data']
    data['result'] = json.dumps(data['result'])
    if execute_result['status'] == 'ok':
        return data
    else:
        return execute_result['data']